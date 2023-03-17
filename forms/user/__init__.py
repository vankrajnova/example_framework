import pytest

pytest.register_assert_rewrite("forms.user.form_user_new")
pytest.register_assert_rewrite("forms.user.form_user_list")
pytest.register_assert_rewrite("forms.user.form_user_card")
pytest.register_assert_rewrite("forms.user.tab_base_info")