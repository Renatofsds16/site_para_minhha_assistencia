from django.contrib.auth.mixins import LoginRequiredMixin

class EmpresaMixin(LoginRequiredMixin):
    """
    Mixin padrão para views multiempresa
    """

    def get_empresa(self):
        return self.request.user.perfil.empresa
