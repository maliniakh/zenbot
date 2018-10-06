var request = require('request')
var rp = require('request-promise')

let lbStrgy = fibonacciLbStrtgy;
module.exports = function container(get, set, clear) {
  return {
    name: 'rm',
    description: 'for rapidminer',

    getOptions: function () {
      this.option('period', 'period length', String, '30m')
      this.option('constant', 'constant', Number, 0.015)
      this.option('cci_periods', 'number of RSI periods', Number, 14)
      this.option('rsi_periods', 'number of RSI periods', Number, 14)
      this.option('srsi_periods', 'number of RSI periods', Number, 9)
      this.option('min_periods', 'min. number of history periods', Number, 30)
      this.option('srsi_k', '%K line', Number, 5)
      this.option('srsi_d', '%D line', Number, 3)
    },

    calculate: function (s) {
      get('lib.ema')(s, 'trend_ema', s.options.min_periods)
      if (typeof s.period.trend_ema !== 'undefined')
        s.trend = s.period.trend_ema > s.lookback[0].trend_ema ? 'up' : 'down'

      // compute Stochastic RSI
      get('lib.srsi')(s, 'srsi', s.options.rsi_periods, s.options.srsi_k, s.options.srsi_d)

      // compute CCI
      // todo: cci_periods zrobic
      get('lib.cci')(s, 'cci', s.options.cci_periods, s.options.constant)

      if (typeof s.period.cci !== 'undefined' && typeof s.period.srsi_K !== 'undefined') {
        s.cci_fromAbove = s.period.cci < s.lookback[0]['cci']
        s.rsi_fromAbove = s.period.srsi_K < s.lookback[0]['srsi_K']
      }

      if (s.period.trend_ema && s.lookback[0] && s.lookback[0].trend_ema) {
        s.period.acc = Math.abs((s.period.trend_ema - s.lookback[0].trend_ema) / s.lookback[0].trend_ema * 100)
      }
    },


    onPeriod: function (s, cb) {
      // todo: s.lookback jest puste :( Array[0]
      // tzn jest wypelniane w kolejnych callach

      if(!s.lookback || s.lookback.length -1 < lbStrgy().maxLookback) {
        cb();
        return;
      }

      var lbPeriods = {};
      let normFactor = s.lookback[0].close; // do normalizacji

      for (var step = 0; step < lbStrgy().maxStep; step++) {
        let lbStep = lbStrgy().strtgy(step); // ile krokow wstecz
        let lb = s.lookback[lbStep];
        lbPeriods['back' + lbStep + '.low'] = lb.low / normFactor;
        lbPeriods['back' + lbStep + '.high'] = lb.high / normFactor;
        lbPeriods['back' + lbStep + '.open'] = lb.open / normFactor;
        lbPeriods['back' + lbStep + '.close'] = lb.close / normFactor;
        lbPeriods['back' + lbStep + '.volume'] = lb.volume / normFactor;
        if(step < 5) {
          lbPeriods['back' + lbStep + '.rsi_avg_gain'] = lb.rsi_avg_gain;
          lbPeriods['back' + lbStep + '.rsi_avg_loss'] = lb.rsi_avg_loss;
          lbPeriods['back' + lbStep + '.rsi'] = lb.rsi;
          lbPeriods['back' + lbStep + '.cci'] = lb.cci;
          lbPeriods['back' + lbStep + '.srsi_D'] = lb.srsi_D;
          lbPeriods['back' + lbStep + '.srsi_K'] = lb.srsi_K;
        }
      }
      Object.keys(lbPeriods).forEach(function(k) {
        if(lbPeriods[k] === undefined) {
          lbPeriods[k] = null;
        }
      });

      // resultArr.push({period: lbPeriods});

      // request.post({
      //     url: 'http://localhost:8080/model',
      //     json: lbPeriods
      //   },
      //   function (error, response, body) {
      //     console.log(body)
      //   });

      var options = {
        method: 'POST',
        uri: 'http://localhost:8080/model',
        body: lbPeriods,
        json: true // Automatically stringifies the body to JSON
      };
      rp(options)
        .then(function (parsedBody) {
          var predictionKey = Object.keys(parsedBody).find(k => {return k.startsWith('prediction')});
          if(parsedBody[predictionKey] === 'up') {
            s.signal = 'buy';
            console.log('buying')
            console.log(parsedBody)
          } else if(parsedBody[predictionKey] === 'down') {
            s.signal = 'sell';
            console.log('selling')
            console.log(parsedBody)
          }

          // console.log(parsedBody)
          cb();
        })
        .catch(function (err) {
          console.log(err)
        });

    },

    onReport: function (s) {
      var cols = []
      return cols
    }

  }
}

let fibonacciArr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 15, 17, 19, 21, 24, 27, 30, 34, 40, 55, 77, 89, 120, 144, 160, 190, 233, 270, 300, 350, 400, 500, 600];

function fibonacciLbStrtgy() {
  return {
    maxStep: fibonacciArr.length,
    maxLookback: fibonacciArr[fibonacciArr.length - 1],
    strtgy: function (step) {
      return fibonacciArr[step];
    }
  }
}
