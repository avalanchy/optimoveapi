class Integrations(object):
    """Namespace class all external system integration-related functions"""

    def __init__(self, transport):
        self._transport = transport

    def add_promotions(self, promotions):
        path = 'integrations/AddPromotions'
        data = [
            {
                'PromoCode': code,
                'PromotionName': name,
            }
            for code, name in promotions.items()
        ]
        return self._transport.post(path, data)

    def get_promotions(self):
        path = 'integrations/GetPromotions'
        return self._transport.get(path)

    def delete_promotions(self, codes):
        path = 'integrations/DeletePromotions'
        data = [
            {'PromoCode': code}
            for code in codes
        ]
        return self._transport.post(path, data)
