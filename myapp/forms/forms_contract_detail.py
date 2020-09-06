from .utils import *
import datetime


class ContractDetailForm(ModelForm):
    field_order = ['id',
                   'src_owner_bank_account_id',
                   'dst_owner_bank_account_id',
                   'value_in_rial',
                   'remittance_currency',
                   'judge_name',
                   'judge_national_id',
                   'judge_vote',
                   'remittance_value',
                   'settlement_type',
                   'expire_date',
                   'status',
                   'description'
                   ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id'] = forms.IntegerField(disabled=True, label="شناسه", initial=self.instance.id)
        # self.fields['expire_date'].widget.attrs['disabled'] = True
        self.fields['settlement_type'].widget.attrs['disabled'] = True
        self.fields['value_in_rial'].widget.attrs['disabled'] = True
        self.fields['remittance_currency'].widget.attrs['disabled'] = True
        self.fields['remittance_value'].widget.attrs['disabled'] = True
        self.fields['judge_vote'].widget.attrs['disabled'] = True
        self.fields['status'].widget.attrs['disabled'] = True
        self.fields['description'].widget.attrs['disabled'] = True
        self.fields['expire_date'] = forms.CharField(max_length=50,
                                                     required=False,
                                                     label="تاریخ اعتبار",
                                                     disabled=True,
                                                     initial=str(datetime.datetime.fromtimestamp(self.instance.expire_date).strftime("%Y/%m/%d")))

    def hide_judge_vote_field(self):
        self.fields['judge_vote'].widget = forms.HiddenInput()

    # def display_judge_vote_and_status(self):
    #     self.fields['judge_vote'].widget = forms.TextInput()
    #     self.fields['status'].widget = forms.TextInput()

    def __add_judge_information_fields(self):
        self.fields['judge_name'] = forms.CharField(max_length=50,
                                                    required=False,
                                                    label="نام داور",
                                                    disabled=True,
                                                    initial=self.instance.judge_name)

        self.fields['judge_national_id'] = forms.CharField(max_length=100,
                                                           required=False,
                                                           label="شناسه ملی داور",
                                                           disabled=True,
                                                           initial=self.instance.judge_national_id)

    def __add_src_owner_field(self):
        self.fields['src_owner_bank_account_id'] = forms.CharField(max_length=50,
                                                                   required=False,
                                                                   label="شماره حساب واردکننده",
                                                                   disabled=True,
                                                                   initial=self.instance.src_owner_bank_account_id)
        self.order_fields(field_order=self.field_order)

    def __add_dst_owner_fields(self):
        self.fields['dst_owner_bank_account_id'] = forms.CharField(max_length=50,
                                                                   required=False,
                                                                   label="شماره حساب صراف",
                                                                   disabled=True,
                                                                   initial=self.instance.dst_owner_bank_account_id)

    def perform_importer_point_of_view(self):
        self.__add_judge_information_fields()
        self.__add_dst_owner_fields()
        self.order_fields(field_order=self.field_order)

    def perform_exchanger_point_of_view(self):
        self.__add_judge_information_fields()
        self.__add_src_owner_field()
        self.order_fields(field_order=self.field_order)

    class Meta:
        model = NormalContract
        fields = [
            'value_in_rial',
            'remittance_currency',
            'remittance_value',
            'settlement_type',
            'judge_vote',
            'status',
            'description',
        ]
        labels = {
            'value_in_rial': 'مبلغ به ریال',
            'remittance_currency': 'ارز حواله',
            'remittance_value': 'مبلغ حواله',
            'settlement_type': 'نوع تسویه',
            'judge_vote': 'رای داور',
            'expire_date': 'تاریخ اعتبار2',
            'status': 'وضعیت',
            'description': 'توضیحات',
        }
