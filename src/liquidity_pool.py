from typing import Dict


class LP:
    liquidity_providers: Dict[str, Dict[str, float]] = {}  # {adr:{c1:amt,c2:amt}}

    def __init__(self, coin1: str, coin2: str, coin1_amt: float, coin2_amt: float):
        self.c1_name = coin1
        self.c2_name = coin2
        self.c1_amt = coin1_amt
        self.c2_amt = coin2_amt
        self.k = coin1_amt * coin2_amt

    def add_liquidity(self, amt_c1: float, amt_c2: float, adr: str):
        try:
            self.liquidity_providers[adr]["c1"] += amt_c1
            self.liquidity_providers[adr]["c2"] += amt_c1
        except:
            self.liquidity_providers[adr]["c1"] = amt_c1
            self.liquidity_providers[adr]["c2"] = amt_c1
        if self.c1_amt / self.c2_amt == amt_c1 / amt_c2:
            self.c1_amt += amt_c1
            self.c2_amt += amt_c2
            self.k = self.c1_amt * self.c2_amt
        else:
            raise Exception("not balanced ratio of amounts")
        return self.liquidity_providers[adr]

    def trade(self, name: str, amt: float):
        # (x+x_1)*(y+y_1)=k
        # k/(x+x_1) - y
        fee = amt * 0.003
        amt -= fee

        if name == self.c1_name:
            total = sum(v["c1"] for _, v in self.liquidity_providers.items())
            for k, v in self.liquidity_providers.items():
                self.liquidity_providers[k]["c1"] += fee * v["c1"] / total
            return_amt = self.k / (self.c1_amt + amt) - self.c2_amt
            self.c1_amt += amt
            self.c2_amt -= return_amt
            return return_amt
        else:
            total = sum(v["c2"] for _, v in self.liquidity_providers.items())
            for k, v in self.liquidity_providers.items():
                self.liquidity_providers[k]["c2"] += fee * v["c2"] / total
            return_amt = self.k / (self.c2_amt + amt) - self.c1_amt
            self.c2_amt += amt
            self.c1_amt -= return_amt
            return return_amt
