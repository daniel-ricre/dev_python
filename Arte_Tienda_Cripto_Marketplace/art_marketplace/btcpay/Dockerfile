FROM btcpayserver/btcpayserver:1.13.6
EXPOSE 49392
ENV BTCPAY_POSTGRES="User ID=btcpay;Password=btcpay_password;Host=btcpay-postgres;Port=5432;Database=btcpay"
ENV BTCPAY_NETWORK=arbitrum-sepolia
ENV BTCPAY_CHAINS="btc,arbitrum"
ENV BTCPAY_BIND=0.0.0.0:49392
ENV BTCPAY_EXTERNALURL=http://localhost:49392
ENV BTCPAY_ROOTPATH=/
