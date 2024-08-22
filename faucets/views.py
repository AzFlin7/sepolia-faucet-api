from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Log
from .serializers import LogSerializer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    
    @action(detail=False, methods=['post'], url_path='fund')
    def fund(self, request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            to_addr = request.data.get('wallet_address')

            try:
                last_record = Log.objects.filter(Q(ip_address=ip) | Q(wallet_address=to_addr)).latest('created_at')
            except Log.DoesNotExist:
                last_record = None
                
            if last_record and (timezone.now() - last_record.created_at > timedelta(minutes=1)):
                w3 = Web3(Web3.HTTPProvider(settings.INFURA_ENDPOINT))
                mnemo = Mnemonic('english')
                seed = mnemo.to_seed(settings.MNEMONIC)
                Account.enable_unaudited_hdwallet_features()
                account = Account.from_mnemonic(settings.MNEMONIC)
                nonce = w3.eth.get_transaction_count(account.address)
                signed_tx = w3.eth.account.sign_transaction({
                    'nonce': nonce,
                    'to': to_addr,
                    'value': w3.to_wei(settings.FAUCET_AMOUNT, 'ether'),
                    'gas': 200000,
                    'gasPrice': w3.to_wei('50', 'gwei'),
                    'chainId': 11155111
                }, account.key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_str = tx_hash.hex()

                Log.objects.create(
                    ip_address=ip,
                    wallet_address=to_addr,
                    transaction_id=tx_str,
                    status='success'
                )
                return Response({'transaction_id': tx_str}, status=status.HTTP_201_CREATED)
            
            else:
                Log.objects.create(
                    ip_address=ip,
                    wallet_address=to_addr,
                    transaction_id='',
                    status='failed'
                )
                return Response({'error': 'Too many requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
                
        except Exception as e:
            Log.objects.create(
                ip_address=ip,
                wallet_address=to_addr,
                transaction_id='',
                status='failed'
            )
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        success_count = Log.objects.filter(status='success').count()
        failed_count = Log.objects.filter(status='failed').count()

        stats = {
            'success_count': success_count,
            'failed_count': failed_count,
        }

        return Response(stats, status=status.HTTP_200_OK)