module.exports = function container (get, set, clear) {
  return {
    name: 'rm',
    description: 'for rapidminer',

    getOptions: function () {
      this.option('period', 'period length', String, '30m')
    },

    calculate: function (s) {
    },

    onPeriod: function (s, cb) {
      cb()
    },

    onReport: function (s) {
      var cols = []
      return cols
    }

}
