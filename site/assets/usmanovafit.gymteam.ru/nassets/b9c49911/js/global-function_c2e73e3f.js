function addGlobalCheckbox(element) {
    var checkOnlyRegister = false;

    if (element.find('.register-form.state-form').length > 0) {
        element = element.find('.register-form.state-form');
        checkOnlyRegister = true;
    }

    if (element.find('.login-form.state-form').length > 0 && !checkOnlyRegister) {
        return function (params) {
            return true;
        };
    }

    if (element.find('.form-content').length > 0) {
        element = element.find('.form-content');
    }

    function hasFormPaidOrder() {
        var formPositionSum = 0;

        element.find(".form-position-input, input[name='formParams[setted_offer_id]'], input.offer-select-input").each(
            function () {
                formPositionSum += $(this).data("price-value");
            }
        );

        if (formPositionSum > 0) {
            return true;
        }

        if (element.parent("form").find('input[name="formParams[willCreatePaidDeal]"]').val() > 0) {
            return true;
        }

        return false;
    }

    var isOfertaCheckboxEnabled = window.globalCheckboxEnabled;

    if (window.hasOwnProperty("globalCheckboxForPaidOnly")) {
        if (window.globalCheckboxForPaidOnly && !hasFormPaidOrder()) {
            isOfertaCheckboxEnabled = false;
        }
    }

    if (isOfertaCheckboxEnabled) {
        var checked = window.persodataConfirm ? 'checked' : '';
        var $checkboxEl = $('<div class="global-confirm-checkbox-block confirm-rules-checkbox">' +
            '<label>' +
            '<input class="global-confirm-checkbox" type="checkbox" ' + checked + ' name="globalConfirmCheckbox" >' +
            '<span class="checkbox-text">' + window.globalCheckboxText + '</span>' +
            '</label>' +
            '</div>');

        var $checkboxInput = $checkboxEl.find('input')
        var firstSubmitButton = element.find('button[type=submit]');
        // if (firstSubmitButton.length > 0 && false) {
        //     $checkboxEl.insertBefore(firstSubmitButton)
        // } else {
            $checkboxEl.appendTo(element);
        // }
    }

    if (window.pdpCheckboxEnabled) {
        var isPdpChecked = window.pdpConfirmedByDefault ? 'checked' : '';
        var $pdpCheckboxEl = $('<div class="global-confirm-checkbox-block confirm-rules-checkbox">' +
            '<label>' +
            '<input class="global-confirm-checkbox" type="checkbox" ' + isPdpChecked + ' name="pdpConfirmCheckbox" >' +
            '<span class="checkbox-text">' + window.pdpCheckboxText + '</span>' +
            '</label>' +
            '</div>');

        var $pdpCheckboxInput = $pdpCheckboxEl.find('input')

        $pdpCheckboxEl.appendTo(element);
    }

    var isMailingCheckboxEnabled = window.checkboxMailingEnabled;
    if (window.hasOwnProperty("checkboxMailingForPaidOnly")) {
        if (window.checkboxMailingForPaidOnly && !hasFormPaidOrder()) {
            isMailingCheckboxEnabled = false;
        }
    }

    if (isMailingCheckboxEnabled) {
        var checked = window.checkboxMailingChecked ? 'checked' : '';
        var input = '<div class="xdget-formField">' +
            '<label>' +
            '<input type="checkbox" ' + checked + ' class="append-handle-input" name="confirmMailingCheckbox" />' +
            '<span class="checkbox-text">' + window.checkboxMailingText + '</span>' +
            '</label>' +
            '</div>';

        var checkboxMailing = $(input);

        if (element.find('.confirm-rules-checkbox').length === 1) {
            checkboxMailing.appendTo(element.find('.confirm-rules-checkbox'));
        } else {
            checkboxMailing = $('<div class="global-confirm-checkbox-block confirm-mailing-checkbox">' + input + '</div>');

            var firstSubmitButton = element.find('button[type=submit]');
            checkboxMailing.appendTo(element);
        }
    }

    return function (params) {
        var str = "";
        if (isOfertaCheckboxEnabled && !$checkboxInput.prop('checked')) {
            if (checkOnlyRegister && !(params && params.state == "register")) {
                return true;
            }

            str = 'Чтобы отправить форму вы должны согласиться с условиями договора-оферты. '
                + 'Отметьте соответствующую галочку';

            if (window.hasOwnProperty("isLegalReworkFeatureEnabled")) {
                if (window.isLegalReworkFeatureEnabled === true) {
                    str = "Чтобы продолжить, необходимо согласиться с условиями оферты";
                }
            }

            if (typeof Yii != 'undefined') {
                str = Yii.t('common', str);
            }

            alert(str);

            return false;
        }

        if (window.pdpCheckboxEnabled && !$pdpCheckboxInput.prop('checked')) {
            if (checkOnlyRegister && !(params && params.state == "register")) {
                return true;
            }

            str = 'Чтобы отправить форму вы должны согласиться с условиями на обработку персональных данных. '
                + 'Отметьте соответствующую галочку';

            if (window.hasOwnProperty("isLegalReworkFeatureEnabled")) {
                if (window.isLegalReworkFeatureEnabled === true) {
                    str = "Чтобы продолжить, необходимо согласиться с условиями обработки персональных данных";
                }
            }

            if (typeof Yii != 'undefined') {
                str = Yii.t('common', str);
            }

            alert(str);

            return false;
        }

        if (isMailingCheckboxEnabled) {
            var isRequired = false;
            if (window.hasOwnProperty("isMailingCheckboxRequired")) {
                if (window.isMailingCheckboxRequired) {
                    isRequired = true;
                }
            }

            if (window.hasOwnProperty("isMailingCheckboxRequiredForNotPaid")) {
                if (window.isMailingCheckboxRequiredForNotPaid && !hasFormPaidOrder()) {
                    isRequired = true;
                }
            }

            if (isRequired) {
                if (!checkboxMailing.find("input").prop("checked")) {
                    if (checkOnlyRegister && !(params && params.state == "register")) {
                        return true;
                    }

                    str = "Для того, чтобы мы могли отправлять вам сообщения на почту, "
                        + "необходимо согласиться на получение писем";

                    if (typeof Yii != 'undefined') {
                        str = Yii.t('common', str);
                    }

                    alert(str);

                    return false;
                }
            }
        }

        return true;
    };
}

function fillCustomFields(settings) {
    var isUtmAutoMapEnabled = !!settings.isUtmAutoMap;
    var fields = settings.fields ? settings.fields : {};

    var utmFields = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    var contexts = ['user', 'deal'];

    function fillUtmField(name, value) {
        var fields = [];
        var nameWithPrefix = 'gc_system.' + name;
        var selector = '[data-element="custom-field"][data-title="' + nameWithPrefix + '"]';
        var $field = $(selector).eq(0);

        if ($field.length) {
            fields.push($field);
        }

        for (var context of contexts) {
            nameWithPrefix = 'gc_system_' + context + '_' + name;
            selector = '[data-element="custom-field"][data-title="' + nameWithPrefix + '"]';
            $field = $(selector).eq(0);

            if ($field.length) {
                fields.push($field);
            }
        }

        if (!fields.length) {
            console.error('Utm field ' + name + ' not found');

            return;
        }

        for (var $f of fields) {
            $input = $f.find('input').eq(0);

            if (!$input.length) {
                continue;
            }

            $input.val(value);
            $input.trigger('change');
        }
    }

    function fillUtmFieldAuto(name) {
        var searchParams = new URLSearchParams(window.location.search);
        var value = searchParams.get(name);

        if (!value) {
            value = '';
        }

        fillUtmField(name, value);
    }

    if (isUtmAutoMapEnabled) {
        for (var utmField of utmFields) {
            fillUtmFieldAuto(utmField);
        }
    }

    for (var id of Object.keys(fields)) {
        var isUtmField = utmFields.includes(id);
        var selector = '';
        var $field = null;
        var value = fields[id];

        if (isUtmField) {
            fillUtmField(id, value);

            continue;
        }

        selector = '[data-element="custom-field"][data-id="' + id + '"]';
        $field = $(selector).eq(0);

        if (!$field.length) {
            console.error('Custom field with id ' + id + ' not found');

            continue;
        }

        var type = $field.data('type');
        var $input;

        switch (type) {
            case 'string':
            case 'date':
            case 'numeric': {
                $input = $field.find('input').eq(0);

                if (!$input) {
                    continue;
                }

                $input.val(value);

                break;
            }
            case 'text': {
                $input = $field.find('textarea').eq(0);

                if (!$input) {
                    continue;
                }

                $input.val(value);

                break;
            }
            case 'checkbox': {
                $input = $field.find('input[type="checkbox"]').eq(0);

                if (!$input) {
                    continue;
                }

                $input.prop('checked', Boolean(value));

                break;
            }
            case 'select': {
                $input = $field.find('select').eq(0);

                if (!$input) {
                    continue;
                }

                var $options = $input.find('option');
                var valueToSelect;

                $options.each(function (_, $option) {
                    var optionValue = $option.value;

                    if (optionValue === value) {
                        valueToSelect = optionValue;
                    }
                });

                if (!valueToSelect) {
                    console.error('Value ' + value + ' is not exist in select field with id ' + id);

                    continue;
                }

                $input.val(valueToSelect);

                break;
            }
            case 'file': {
                console.error('File field type is not supported. Field id ' + id);

                continue;
            }
            case 'multi_select': {
                if (!Array.isArray(value)) {
                    console.error('Value must an array for field with multi_select type. Field id ' + id);

                    continue;
                }

                var $checkboxes = $field.find('input[type="checkbox"]');

                $checkboxes.each(function (_, checkbox) {
                    var $checkbox = $(checkbox);

                    if (value.includes($checkbox.val())) {
                        $checkbox.prop('checked', true);
                    } else {
                        $checkbox.prop('checked', false);
                    }

                    $checkbox.trigger('change');
                });

                break;
            }
            default:
                console.error('Unknown field type. Field id ' + id);

                continue;
        }

        if ($input) {
            $input.trigger('change');
        }
    }
}
