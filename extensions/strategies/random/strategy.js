let z = require('zero-fill')
let n = require('numbro')

module.exports = function container (get, set, clear) {
  return {
    name: 'random',
    description: 'Random trading all in',

    getOptions: function () {
      this.option('period', 'period length', String, '5s')
      this.option('chance', '1 / chance of buying or selling', String, '100')
      this.option('constant', 'constant', Number, 0.015)
      this.option('cci_periods', 'number of RSI periods', Number, 14)
      this.option('rsi_periods', 'number of RSI periods', Number, 14)
      this.option('srsi_periods', 'number of RSI periods', Number, 9)
      this.option('min_periods', 'min. number of history periods', Number, 30)
      this.option('srsi_k', '%K line', Number, 5)
      this.option('srsi_d', '%D line', Number, 3)
    },

    /**
     * wolane w engine.onTrade
     * @param s
     */
    calculate: function (s) {
      if (s.lookback[1]) {
        s.period.speed = (s.period.close - s.lookback[1].close) / s.lookback[1].close * 100
        s.period.abs_speed = Math.abs((s.period.close - s.lookback[1].close) / s.lookback[1].close * 100)
        if (s.lookback[s.options.baseline_periods + 1]) {
          get('lib.ema')(s, 'baseline', s.options.baseline_periods, 'abs_speed')
        }

        /* oscylatory */
        get('lib.ema')(s, 'trend_ema', s.options.min_periods)
        if (typeof s.period.trend_ema !== 'undefined')
          s.trend = s.period.trend_ema > s.lookback[0].trend_ema ? 'up' : 'down'
        // compute Stochastic RSI
        get('lib.srsi')(s, 'srsi', s.options.rsi_periods, s.options.srsi_k, s.options.srsi_d)
        // compute CCI
        get('lib.cci')(s, 'cci', s.options.cci_periods, s.options.constant)
        if (typeof s.period.cci !== 'undefined' && typeof s.period.srsi_K !== 'undefined') {
          s.cci_fromAbove = s.period.cci < s.lookback[0]['cci']
          s.rsi_fromAbove = s.period.srsi_K < s.lookback[0]['srsi_K']
        }
        if (s.period.trend_ema && s.lookback[0] && s.lookback[0].trend_ema) {
          s.period.acc = Math.abs((s.period.trend_ema - s.lookback[0].trend_ema) / s.lookback[0].trend_ema * 100)
        }
      }
    },

    /**
     * ustawiane na s:
     *  s.oversold
        //s.trend = 'oversold'
        s.signal = 'buy|sell' - chyba tylko ten jest wymagany
        s.cancel_down = true
         acted_on_stop = false
         acted_on_trend = true
         action = null
         asset = "ETH"
         balance = Object
         ctx = Object
         currency = "USDT"
         day_count = 2
         exchange = Object
         in_preroll = false
         last_buy_price = "222.39003050"
         last_day = Bucket
         last_period_id = "5s300140122"
         last_sell_price = "222.31091505"
         last_signal = "sell"
         last_trade_worth = -0.010299021797850248
         lookback = Array[1482]
         my_trades = Array[55]
         options = Object
         period = Object
         product = Object
         product_id = "ETH-USDT"
         selector = "poloniex.ETH-USDT"
         signal = null
         start_capital = 1000
         start_price = 216.57272
         strategy = Object
         vol_since_last_blink = 15878.803695300056
         __proto__ = Object
     * @param s
     * @param cb
     */
    onPeriod: function (s, cb) {
      // if (typeof s.period.baseline === 'number') {
      //   if (s.period.speed >= s.period.baseline * s.options.trigger_factor) {
      //     if (s.trend !== 'up') {
      //       s.acted_on_trend = false
      //     }
      //     s.trend = 'up'
      //     s.signal = !s.acted_on_trend ? 'buy' : null
      //   }
      //   else if (s.period.speed <= s.period.baseline * s.options.trigger_factor * -1) {
      //     if (s.trend !== 'down') {
      //       s.acted_on_trend = false
      //     }
      //     s.trend = 'down'
      //     s.signal = !s.acted_on_trend ? 'sell' : null
      //   }
      // }

      let rand = Math.random();
      if(rand < 0.01) {
        s.signal = 'buy'
      } else if (rand > 0.09) {
        s.signal = 'sell'
      } else {
        s.signal = null
      }



      cb()
    },

    onReport: function (s) {
      var cols = []
      cols.push(z(8, n(s.period.speed).format('0.0000'), ' ')[s.period.speed >= 0 ? 'green' : 'red'])
      if (typeof s.period.baseline === 'number') {
        cols.push(z(8, n(s.period.baseline).format('0.0000'), ' ').grey)
      }
      return cols
    }
  }
}
