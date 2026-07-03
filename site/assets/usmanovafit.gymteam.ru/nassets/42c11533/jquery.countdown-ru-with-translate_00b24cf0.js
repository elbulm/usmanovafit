function ct(value) {
	if (typeof Yii != 'undefined') {
		value = Yii.t('common', value);
	}

	return value;
}

(function($) {
	$.countdown.regionalOptions['ru'] = {
		labels: [ct('Лет'), ct('Месяцев'), ct('Недель'), ct(' дней '), ':', ':', ''],
		labels1: [ct('Год'), ct('Месяц'), ct('Неделя'), ct(' день '), ':', ':', ''],
		labels2: [ct('Года'), ct('Месяца'), ct('Недели'), ct(' дня '), ':', ':', ''],
		compactLabels: [ct('л'), ct('м'), ct('н'), ct(' д')],
		compactLabels1: [ct('л'), ct('м'), ct('н'), ct(' д')],
		whichLabels: function (amount) {
			var units = amount % 10;
			var tens = Math.floor((amount % 100) / 10);
			return (amount == 1 ? 1 : (units >= 2 && units <= 4 && tens != 1 ? 2 :
				(units == 1 && tens != 1 ? 1 : 0)));
		},
		digits: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		timeSeparator: ':',
		isRTL: false
	};
	$.countdown.setDefaults($.countdown.regionalOptions['ru']);
})(jQuery);
