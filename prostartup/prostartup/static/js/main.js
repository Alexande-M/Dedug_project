$(function () {
	$('.services__slider').slick({
		infinite: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		arrows: false,
		autoplay: true,
		autoplaySpeed: 1500,
		responsive: [{
			breakpoint: 680,
			settings: {
				infinite: true,
				slidesToShow: 1,
				slidesToScroll: 1,
				centerMode: true,
			}
		}]
	});


	var btn = $('.top-button');

	$(window).scroll(function () {
		if ($(window).scrollTop() > 500) {
			btn.addClass('show');
		} else {
			btn.removeClass('show');
		}
	});

	btn.on('click', function (e) {
		e.preventDefault();
		$('html, body').animate({
			scrollTop: 0
		}, '300');
	});

	$('.belive__carousel').slick({
		infinite: true,
		slidesToShow: 5,
		slidesToScroll: 1,
		arrows: false,
		autoplay: true,
		autoplaySpeed: 1500,
		responsive: [{
			breakpoint: 1380,
			settings: {
				infinite: true,
				slidesToShow: 3,
				slidesToScroll: 1
			}
		},
		{
			breakpoint: 780,
			settings: {
				infinite: true,
				slidesToShow: 3,
				slidesToScroll: 1
			}
		},
		{
			breakpoint: 680,
			settings: {
				infinite: true,
				slidesToShow: 2,
				slidesToScroll: 1,
				arrows: false
			}
		},
		{
			breakpoint: 480,
			settings: {
				infinite: true,
				slidesToShow: 1,
				slidesToScroll: 1,
				arrows: false
			}
		}
		]
	});


	var show_menu = $('.header__nvigation-btn');
	var close_menu = $('.close__btn');
	var show_menuMob = $('.header__nvigation-btn__mob');
	var close_menuMob = $('.close__btn-mob');
	var navigation = $('.header__navigation');
	show_menu.on('click', function (event) {
		navigation.addClass('active');
		show_menu.css('display', 'none');
		$('.header__navigation-lang').css('display', 'none');
		$('.menu').css('display', 'block');
		$('.close__btn').css('display', 'block');
		$('.header__navigation-social').css('display', 'block');
	});

	close_menu.on('click', function () {
		navigation.removeClass('active')
		close_menu.css('display', 'none');
		$('.header__navigation-social').css('display', 'none');
		$('.menu').css('display', 'none');
		show_menu.css('display', 'block');
		$('.header__navigation-lang').css('display', 'flex');
	});

	show_menuMob.on('click', function () {
		navigation.addClass('active')
		show_menuMob.css('display', 'none');
		$('.menu').css('display', 'block');
		close_menuMob.css('display', 'block');
	});

	close_menuMob.on('click', function () {
		navigation.removeClass('active')
		close_menuMob.css('display', 'none');
		$('.menu').css('display', 'none');
		show_menuMob.css('display', 'block');
	});

	var modal = $('.modal');
	var open = $('#registration-modal');
	var close = $('#close-modal');

	open.on('click', function () {
		modal.fadeIn(350);
	});

	close.on('click', function () {
		modal.fadeOut(350);
	});

	modal.click(function (e) {
		if ($(e.target).closest('.modal__registration').length == 0) {
			$(this).fadeOut(350);
		}
	});

	var costInvest = $('.costInvest');
	var periodInvest = $('.periodInvest');
	var costBuyer = $('.costBuyer');
	var periodBuyer = $('.periodBuyer');
	$('select#subscriptionInv').change(function () {
		var el = $(this).val();
		if (el == 1) {
			costInvest.text('680₽');
			periodInvest.text('1 месяц');
		}
		if (el == 2) {
			costInvest.text('1099₽');
			periodInvest.text('2 месяца');
		}
		if (el == 3) {
			costInvest.text('1619₽');
			periodInvest.text('3 месяца');
		}
	});

	$('select#subscriptionBuy').change(function () {
		var el = $(this).val();
		if (el == 1) {
			costBuyer.text('399₽');
			periodBuyer.text('1 месяц');
		}
		if (el == 2) {
			costBuyer.text('638₽');
			periodBuyer.text('2 месяца');
		}
		if (el == 3) {
			costBuyer.text('1120₽');
			periodBuyer.text('3 месяца');
		}
	});

	var showNavbar = $('.burger-btn');
	var adminNavbar = $('.admin__nav');
	var closeAdmin = $('.admin__content');

	showNavbar.on('click', function () {
		adminNavbar.addClass('active-nav')
		$('.mobile__btns').css('bottom', '-200px');
	});


	// ЗАКРЫТИЕ ПРИ НАЖАТИИ ВНЕ МЕНЮ

	$(document).mouseup(function (e) {
		if (!adminNavbar.is(e.target) && adminNavbar.has(e.target).length === 0) {
			adminNavbar.removeClass('active-nav');
		}
	});

	// ФИЛЬТР
	var filter = $('.filter');
	var filterBtn = $('#filter-btn');

	filterBtn.on('click', function () {
		$('.mobile__btns').css('bottom', '-200px');
		filter.css('bottom', '0');
	});

	$(document).mouseup(function (e) {
		if (!filter.is(e.target) && filter.has(e.target).length === 0) {
			filter.css('bottom', '-1000px');
			$('.mobile__btns').css('bottom', '10px');
		}
	});


	// Загрузка картинок

	function addImg(e) {
		$(e).change(function () {
			var value = $(e).val();
			var inputSrc = e + ' + label .js-value';
			$(inputSrc).text(value);
		});
	}

	addImg('#add-img1')
	addImg('#add-img2')
	addImg('#add-img3')


	$('#presentation').change(function () {
		var value = $('#presentation').val();
		$('#presentation + label').text(value);
	});

	$('#plan').change(function () {
		var value = $('#plan').val();
		$('#plan + label').text(value);
	});

	$('select#type').change(function () {
		var el = $('select#type').val();
		if (el == 'investing') {
			$('#investCost').removeAttr('disabled', 'disabled');
		}
		if (el == 'selling') {
			$('#investCost').attr('disabled', 'disabled');
		}
	});

	//  Вкладки (ТАБЫ)

	$('.js-tab-trigger').click(function () {
		var id = $(this).attr('data-tab'),
			content = $('.js-tab-content[data-tab="' + id + '"]');

		$('.js-tab-trigger.active-tab').removeClass('active-tab');
		$(this).addClass('active-tab');

		$('.js-tab-content.active-tab').removeClass('active-tab');
		content.addClass('active-tab');
	});

	$('#profile-image').change(function () {
		var value = $('#profile-image').val();
		$('#profile-image + label span').text(value);
	});

});