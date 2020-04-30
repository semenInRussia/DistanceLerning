from rest_framework import serializers
# Create your serializers here...

class MessageSerializer(serializers.ModelSerializer):
    from_username = serializers.ReadOnlyField(source='from_user.username')
    to_username = serializers.ReadOnlyField(source='to.username')

    class Meta:
        fields = ['to', 'from_user', 'to_username', 'from_username', 'text', 'subject']
