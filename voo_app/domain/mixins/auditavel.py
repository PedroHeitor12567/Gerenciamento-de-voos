class AuditavelMixin:
    def logs(self, evento:str):
        return f"[LOG] {evento}"