import pytest

from ..models import PreflightResult
from ..serializers import (
    PreflightResultSerializer,
    JobSerializer,
)


@pytest.mark.django_db
class TestPreflightSerializer:
    def test_preflight_error_count(
            self, user_factory, plan_factory, preflight_result_factory):
        user = user_factory()
        plan = plan_factory()
        preflight = preflight_result_factory(
            user=user,
            organization_url=user.instance_url,
            plan=plan,
            results={
                0: [{'status': 'error'}],
            },
            status=PreflightResult.Status.complete,
        )
        serializer = PreflightResultSerializer(instance=preflight).data
        assert serializer["error_count"] == 1
        assert serializer["warning_count"] == 0

    def test_preflight_warning_count(
            self, user_factory, plan_factory, preflight_result_factory):
        user = user_factory()
        plan = plan_factory()
        preflight = preflight_result_factory(
            user=user,
            organization_url=user.instance_url,
            plan=plan,
            results={
                0: [{'status': 'warn'}],
            },
            status=PreflightResult.Status.complete,
        )
        serializer = PreflightResultSerializer(instance=preflight).data
        assert serializer["error_count"] == 0
        assert serializer["warning_count"] == 1

    def test_preflight_is_ready(
            self, user_factory, plan_factory, preflight_result_factory):
        user = user_factory()
        plan = plan_factory()
        preflight = preflight_result_factory(
            user=user,
            organization_url=user.instance_url,
            plan=plan,
            results={
                0: [{'status': 'warn'}],
            },
            status=PreflightResult.Status.complete,
        )
        serializer = PreflightResultSerializer(instance=preflight).data
        assert serializer["is_ready"]

    def test_preflight_is_not_ready(
            self, user_factory, plan_factory, preflight_result_factory):
        user = user_factory()
        plan = plan_factory()
        preflight = preflight_result_factory(
            user=user,
            organization_url=user.instance_url,
            plan=plan,
            results={
                0: [{'status': 'error'}],
            },
            status=PreflightResult.Status.complete,
        )
        serializer = PreflightResultSerializer(instance=preflight).data
        assert not serializer["is_ready"]


@pytest.mark.django_db
class TestJob:
    def test_create_good(
            self, rf, user_factory, plan_factory, step_factory,
            preflight_result_factory):
        plan = plan_factory()
        user = user_factory()
        step1 = step_factory(plan=plan)
        step2 = step_factory(plan=plan)
        step3 = step_factory(plan=plan)
        request = rf.get('/')
        request.user = user
        preflight_result_factory(
            plan=plan,
            user=user,
            status=PreflightResult.Status.complete,
            results={
                step1.id: [{'status': 'warn', 'message': ''}],
                step2.id: [{'status': 'skip', 'message': ''}],
                step3.id: [{'status': 'optional', 'message': ''}],
            },
        )
        data = {
            'plan': plan.id,
            'steps': [step1.id, step2.id, step3.id],
        }
        serializer = JobSerializer(data=data, context=dict(request=request))

        assert serializer.is_valid()

    def test_create_bad(self, rf, user_factory, plan_factory):
        plan = plan_factory()
        user = user_factory()
        request = rf.get('/')
        request.user = user
        data = {
            'plan': plan.id,
            'steps': [],
        }
        serializer = JobSerializer(data=data, context=dict(request=request))

        assert not serializer.is_valid()
