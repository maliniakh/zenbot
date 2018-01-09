let z = require('zero-fill')
let n = require('numbro')

module.exports = function container (get, set, clear) {
  return {
    name: 'random',
    description: 'Random trading all in',

    getOptions: function () {
      this.option('period', 'period length', String, '5s')
      this.option('chance', '1 / chance of buying or selling', String, '100')
    },

    calculate: function (s) {
      if (s.lookback[1]) {
        s.period.speed = (s.period.close - s.lookback[1].close) / s.lookback[1].close * 100
        s.period.abs_speed = Math.abs((s.period.close - s.lookback[1].close) / s.lookback[1].close * 100)
        if (s.lookback[s.options.baseline_periods + 1]) {
          get('lib.ema')(s, 'baseline', s.options.baseline_periods, 'abs_speed')
        }
      }
    },

    /**
     * ustawiane na s:
     *  s.oversold
        //s.trend = 'oversold'
        s.signal = 'buy|sell' - chyba tylko ten jest wymagany
        s.cancel_down = true
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
