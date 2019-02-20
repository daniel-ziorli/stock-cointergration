
class stock_exchange():
    def __init__(self, capital):
        self.capital = capital
        self.shares = 0
        self.commision = 10
        self.bought_price = None
        self.stop_loss_value = -0.99

        self.winners = 0
        self.lossers = 0

        self.equity = []
        self.trade_roi = []

    def update_equity(self, current_price):
        self.equity.append(self.capital + (current_price * self.shares))

    def stop_loss(self, current_price):
        if self.shares > 0:
            roi = (current_price - self.bought_price) / self.bought_price
            if roi < self.stop_loss_value:
                self.sell(self.shares, current_price)
                return True
        return False

    def buy(self, dollar_amount, share_cost):
        if share_cost > 0:
            number_of_shares = (dollar_amount - self.commision) // share_cost
            if number_of_shares > 0:
                self.shares += int(number_of_shares)
                self.capital -= number_of_shares * share_cost
                self.capital -= self.commision
                self.bought_price = share_cost
                return 1

        return -1

    def sell(self, share_amount, share_cost):
        share_amount = int(share_amount)
        if self.shares > 0:
            if (share_amount * share_cost) - self.commision > 0:
                roi = (share_cost - self.bought_price) / self.bought_price
                if roi > 0:
                    self.winners += 1
                else:
                    self.lossers += 1
                self.trade_roi.append(roi)
                self.shares -= share_amount
                self.capital += share_amount * share_cost
                self.capital -= self.commision

        return 1
