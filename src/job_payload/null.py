from job_payload.payload_abstract import PayloadProviderAbstract


class JobPayloadProvider(PayloadProviderAbstract):
    @staticmethod
    def __call__(_):
        return {}
