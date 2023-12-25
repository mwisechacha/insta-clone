class PrepopulateAndDisableUserMixin:
    def get_form(self, request, obj=None, **kwargs):
        form = super(PrepopulateAndDisableUserMixin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].disabled = True
        return form
