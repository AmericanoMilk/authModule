from rest_framework import serializers
from tenant_app.models import Tenant


class TenantLoginSerializer(serializers.Serializer):
    class Meta:
        models = Tenant
        fields = ("tenant", "password")


class TenantRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ("tenant", "password", "name")
        read_only_fields = ('is_superuser', "status")

    def create(self, validated_data):
        return Tenant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    def __repr__(self):
        return self.instance


class TenantSearchSerializer(serializers.Serializer):
    class Meta:
        models = Tenant
        fields = ("tenant", "create_time", "update_time")
