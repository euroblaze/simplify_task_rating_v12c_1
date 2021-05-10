$(document).ready(function () {

    function deselectRateAtt(rate) {
        $(rate).attr('aria-checked', "false");
    }

    function selectRateAtt(rate) {
        $(rate).attr('aria-checked', "true");
    }

    function rateClass(rate) {
        $(rate).toggleClass("fa-star-o fa-star");
    }

    function rateAddClass(rate) {
        if ($(rate).hasClass("fa-star-o")) {
            rateClass(rate);
        }
    }

    function showRateForm() {
        $(".rating-questions-block").click(function () {
            $(".rate-form").toggleClass("d-none d-block");
        });
    }

    function showRateFormLoad() {
        resizeTextArea();
    }

    function showNumberOfQuestions() {
        $(".rating-questions-block span").text($('.rate-question').length)
    }

    function resizeTextArea() {
        $('.rating-block .additional-notes-area').height(
            $('.question-block').height() - 50
        );
    }

    function rateRemoveClass(rate) {
        if ($(rate).hasClass("fa-star")) {
            rateClass(rate);
        }
    }

    function populateRates() {
        $("div.priority_custom_widget").children('input').each(function (i) {
            let choice = $(this).val();
            let rated = false;
            i++;
            $(this).attr("name", `q_${i}`)
            $($(this).parent().children('a').get().reverse()).each(function () {
                if ($(this).attr("data-index") === choice) {
                    selectRateAtt(this);
                    rateClass(this);
                    rated = true;
                } else if (rated === true) {
                    rateClass(this);
                }
            });
        });
    }

    function populateHoverRates() {
        $("a.task-rating")
            .mouseover(function () {
                let rating_option = $(this).attr('data-index');
                $($(this).parent()).children('a').each(function () {
                    if ($(this).attr('data-index') <= rating_option) {
                        rateAddClass(this);
                    } else if ($(this).attr('data-index') > rating_option) {
                        rateRemoveClass(this)
                    }
                });
            })
            .mouseout(function () {
                let rated = false
                $($(this).parent().children('a').get().reverse()).each(function () {
                    if (rated === true) {
                        rateAddClass(this);
                    } else if ($(this).attr('aria-checked') === 'false') {
                        rateRemoveClass(this);
                    } else if ($(this).attr('aria-checked') === 'true') {
                        rateAddClass(this);
                        rated = true;
                    }

                });
            })
            .click(function () {
                if ($(this).attr('aria-checked') === 'true') {
                    deselectRateAtt(this);
                } else {
                    selectRateAtt(this);
                }
                rateTask(this);
            });
    }

    function rateTask(selected_rate) {
        let rated = false;
        $($(selected_rate).parent().children('a').get().reverse()).each(function () {

            if ($(selected_rate).attr('aria-checked') === 'false') {
                rateRemoveClass(this);
                $(this).parent().children('input').each(function () {
                    if ($(this).val() !== "0") {
                        $(this).val("0");
                    }
                });
                deselectRateAtt(this);
            } else if ($(this).is($(selected_rate))) {
                rateAddClass(this)
                let choice = this;
                $(this).parent().children('input').each(function () {
                    $(this).val($(choice).attr('data-index'));
                });
                rated = true;
            } else if ($(this).attr('aria-checked') === 'true' && rated === false) {
                rateRemoveClass(this);
                deselectRateAtt(this);
            } else if ($(this).attr('aria-checked') === 'true' && rated === true) {
                rateAddClass(this);
                deselectRateAtt(this);
            } else if ($(this).attr('aria-checked') === 'false' && rated === true) {
                rateAddClass(this);
            } else if ($(this).attr('aria-checked') === 'false' && rated === false) {
                rateRemoveClass(this);
            }
        });
    }

    populateHoverRates();
    showRateFormLoad();
    showRateForm();
    showNumberOfQuestions();
    populateRates();

});

