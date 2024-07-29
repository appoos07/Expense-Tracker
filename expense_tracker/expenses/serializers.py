from rest_framework import serializers
from .models import User, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number']

class ExpenseSerializer(serializers.ModelSerializer):
    splits = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'split_type', 'participants', 'date_created', 'splits']

    def get_splits(self, obj):
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            amounts = self.context.get('amounts', None)
            percentages = self.context.get('percentages', None)
            return obj.calculate_splits(amounts, percentages)
        return None  # or return some default value, if needed

    def validate(self, data):
        participants = data.get('participants')
        if not participants:
            raise serializers.ValidationError({"participants": "This list may not be empty."})

        split_type = data.get('split_type')
        if split_type == 'PERCENTAGE':
            percentages = self.initial_data.get('percentages', None)
            if percentages is None:
                raise serializers.ValidationError({"percentages": "Percentages are required for split type PERCENTAGE."})
            if sum(percentages) != 100:
                raise serializers.ValidationError({"percentages": "Percentages must sum to 100."})
        elif split_type == 'EXACT':
            amounts = self.initial_data.get('amounts', None)
            if amounts is None:
                raise serializers.ValidationError({"amounts": "Amounts are required for split type EXACT."})
            if len(amounts) != len(participants):
                raise serializers.ValidationError({"amounts": "Number of amounts does not match number of participants."})

        return data
