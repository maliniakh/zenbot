module.exports = {
  _ns: 'zenbot',

  'strategies.random': require('./strategy'),
  'strategies.list[]': '#strategies.random'
}
