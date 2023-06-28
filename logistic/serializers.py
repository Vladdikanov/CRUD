from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','description']
    # настройте сериализатор для продукта
    pass


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ["product", "quantity", "price"]
    # настройте сериализатор для позиции продукта на складе
    pass


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address','positions']

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for pos in positions:
            StockProduct.objects.create(stock=stock,**pos)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for pos in positions:
            StockProduct.stock = stock
            StockProduct.product = pos['product']
            StockProduct.quantity = pos['quantity']
            StockProduct.price = pos['price']
            StockProduct.save()

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
