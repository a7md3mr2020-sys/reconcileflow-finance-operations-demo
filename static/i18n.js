(() => {
  if (document.documentElement.lang !== "ar") return;

  const t = {
    "ReconcileFlow home": "الصفحة الرئيسية لـ ReconcileFlow",
    "Portfolio modules": "وحدات النظام",
    "Language": "اللغة",
    "Standard": "المطابقة العادية",
    "Detailed": "المطابقة العميقة",
    "Invoices": "متابعة الفواتير",
    "Control Center": "مركز العمليات",
    "Report Workshop": "ورشة التقارير",
    "Public demo": "نسخة تجريبية عامة",
    "Finance operations reconciliation": "مطابقة العمليات المالية",
    "Synthetic data only": "بيانات تجريبية فقط",
    "All workflows": "كل المسارات",
    "Back to workspace": "العودة إلى مساحة العمل",
    "Back to detailed workspace": "العودة إلى المطابقة العميقة",
    "Return to workflow hub": "العودة إلى مركز المسارات",
    "FINANCE OPERATIONS PRODUCT CASE STUDY": "دراسة حالة لمنتج عمليات مالية",
    "Three control workflows. One reconciliation platform.": "ثلاثة مسارات رقابية. منصة مطابقة واحدة.",
    "A working marine-tour finance demo for reconciliation, pricing control, invoice follow-up, and configurable reporting.": "عرض عملي لنظام مالي للرحلات البحرية يشمل المطابقة ورقابة التسعير ومتابعة الفواتير والتقارير القابلة للتخصيص.",
    "Try the live standard demo": "جرّب المطابقة العادية مباشرة",
    "Try the live detailed demo": "جرّب المطابقة العميقة مباشرة",
    "Live demo details": "تفاصيل التجربة المباشرة",
    "No login": "بدون تسجيل",
    "Open and interact immediately": "افتح وابدأ التجربة فورًا",
    "Synthetic data": "بيانات تجريبية",
    "Safe public portfolio records": "سجلات آمنة للعرض العام",
    "60-second review": "تجربة في 60 ثانية",
    "Projects, edits, filters, and audit trail": "مشاريع وتعديلات وفلاتر وسجل مراجعة",
    "A portfolio-safe demonstration of a broader marine-tour finance system built around operational reconciliation, detailed pricing control, invoice follow-up, and configurable reporting.": "عرض آمن لنظام مالي متكامل للرحلات البحرية يجمع المطابقة التشغيلية والتسعير التفصيلي ومتابعة الفواتير والتقارير القابلة للتخصيص.",
    "Choose a workflow": "اختر مسار العمل",
    "CORE CONTROL": "الرقابة الأساسية",
    "PRICING CONTROL": "رقابة التسعير",
    "RECEIVABLE CONTROL": "رقابة المستحقات",
    "Standard Reconciliation": "المطابقة العادية",
    "Detailed Reconciliation": "المطابقة العميقة",
    "Invoice Tracking": "متابعة الفواتير",
    "Compare booking references, dates, companies, services, passenger categories, and amounts across two sources.": "قارن أرقام الحجوزات والتواريخ والشركات والخدمات وفئات الركاب والمبالغ بين مصدرين.",
    "Extend the review into trip type, hotel or pickup, transfer state, adult rate, chargeable passengers, and calculated amount.": "وسّع المراجعة لتشمل نوع الرحلة والفندق أو نقطة الالتقاء والترانسفير وسعر البالغ والأفراد المحتسبين والمبلغ المحسوب.",
    "Follow each company from review through invoice preparation, sending, payment, and balance closure.": "تابع كل شركة من المراجعة وحتى إعداد الفاتورة والإرسال والدفع وإغلاق الرصيد.",
    "Missing and duplicate detection": "اكتشاف الحجوزات الناقصة والمكررة",
    "Company-name mapping evidence": "دليل ربط أسماء الشركات",
    "Exception filters and Excel export": "فلاتر الفروقات وتصدير Excel",
    "Automatic rate or amount derivation": "اشتقاق السعر أو المبلغ تلقائيًا",
    "Child at half rate; infant at zero": "الطفل بنصف السعر والرضيع دون تكلفة",
    "Independent reference matching": "مطابقة مستقلة بالرقم المرجعي",
    "Receivable and payable direction": "تحديد الرصيد المستحق أو الدائن",
    "Payment and collection analysis": "تحليل الدفعات والتحصيلات",
    "Stage progress and activity history": "تقدم المراحل وسجل الحركة",
    "Open workflow": "فتح المسار",
    "SIGNATURE FEATURE": "الميزة المميزة",
    "Open Report Workshop": "فتح ورشة التقارير",
    "BEYOND THE THREE CORE PATHS": "أبعد من المسارات الثلاثة الأساسية",
    "The operational control layer": "طبقة الرقابة التشغيلية",
    "Open Operations Control Center": "فتح مركز العمليات",
    "Combined periods": "الفترات المجمعة",
    "Resolved exceptions": "الفروقات المحلولة",
    "No-show value": "قيمة عدم الحضور",
    "Audit coverage": "تغطية المراجعة",
    "Multi-project control": "رقابة المشاريع المجمعة",
    "Resolution tracking": "متابعة الحلول",
    "Settlement ledger": "سجل التسويات",
    "No-show analysis": "تحليل عدم الحضور",
    "Company delivery": "تسليم الشركات",
    "Filter-aware reports": "تقارير مرتبطة بالفلاتر",
    "Load synthetic demo": "تحميل العرض التجريبي",
    "Load detailed demo": "تحميل العرض التفصيلي",
    "Review name": "اسم المراجعة",
    "System A": "النظام أ",
    "System B": "النظام ب",
    "No file selected": "لم يتم اختيار ملف",
    "Run reconciliation": "تشغيل المطابقة",
    "Run detailed reconciliation": "تشغيل المطابقة العميقة",
    "Download sample A": "تحميل نموذج أ",
    "Download sample B": "تحميل نموذج ب",
    "Download detailed A": "تحميل النموذج التفصيلي أ",
    "Download detailed B": "تحميل النموذج التفصيلي ب",
    "Search": "بحث",
    "Status": "الحالة",
    "All statuses": "كل الحالات",
    "Matched": "متطابق",
    "Mismatch": "به اختلاف",
    "Missing in System A": "غير موجود في النظام أ",
    "Missing in System B": "غير موجود في النظام ب",
    "Duplicate detected": "تكرار مكتشف",
    "Daily matching": "المطابقة اليومية",
    "PRIMARY RECONCILIATION": "المطابقة الأساسية",
    "Daily company matching": "مطابقة الشركات يوميًا",
    "Daily company matching by trip type": "مطابقة الشركات يوميًا حسب نوع الرحلة",
    "Date": "التاريخ",
    "Trip type": "نوع الرحلة",
    "Rows A / B": "عدد الصفوف أ / ب",
    "Adults A / B": "البالغون أ / ب",
    "Children A / B": "الأطفال أ / ب",
    "References A / B": "الأرقام المرجعية أ / ب",
    "Transfer rows A / B": "صفوف الترانسفير أ / ب",
    "Calculated amount A / B": "المبلغ المحسوب أ / ب",
    "Calculated variance": "فرق المبلغ المحسوب",
    "Pricing variance A / B": "انحراف التسعير أ / ب",
    "Filtered variance": "إجمالي الفرق بعد الفلترة",
    "Amount difference": "اختلاف مبلغ",
    "Passenger difference": "اختلاف أفراد",
    "Amount and passenger difference": "اختلاف مبلغ وأفراد",
    "System A only": "في النظام أ فقط",
    "System B only": "في النظام ب فقط",
    "Reference": "الرقم المرجعي",
    "References": "الأرقام المرجعية",
    "Differences": "الفروقات",
    "Variance": "الانحراف",
    "Amount variance": "انحراف المبلغ",
    "Pricing variance": "انحراف التسعير",
    "Match rate": "نسبة التطابق",
    "Mismatches": "الاختلافات",
    "Missing": "الناقص",
    "Missing records": "الحجوزات الناقصة",
    "Duplicates": "المكرر",
    "Total references": "إجمالي الأرقام المرجعية",
    "Export full results": "تصدير كل النتائج",
    "Export detailed workbook": "تصدير ملف المطابقة العميقة",
    "Export tracking workbook": "تصدير ملف متابعة الفواتير",
    "Export control workbook": "تصدير ملف مركز العمليات",
    "Record-level results": "نتائج الحجوزات",
    "System A company": "شركة النظام أ",
    "System B company": "شركة النظام ب",
    "System A amount": "مبلغ النظام أ",
    "System B amount": "مبلغ النظام ب",
    "Reference-number reconciliation": "مطابقة الرقم المرجعي",
    "Detailed comparison": "المقارنة التفصيلية",
    "Reference matching": "مطابقة الرقم المرجعي",
    "Pricing and operational exceptions": "فروقات التسعير والتشغيل",
    "Hotel or pickup": "الفندق أو نقطة الالتقاء",
    "No transfer": "بدون ترانسفير",
    "Not present": "غير موجود",
    "Overview": "نظرة عامة",
    "Company tracking": "متابعة الشركات",
    "Company names": "أسماء الشركات",
    "Reconciled": "تمت المطابقة",
    "Payment complete": "تم الدفع",
    "CENTRAL COMPANY REGISTER": "سجل الشركات المركزي",
    "Company names and opening amounts": "أسماء الشركات والأرصدة الأساسية",
    "Company or code...": "اسم الشركة أو الكود...",
    "Invoice total": "إجمالي الفاتورة",
    "New company": "شركة جديدة",
    "Company name": "اسم الشركة",
    "Add company": "إضافة شركة",
    "Filtered totals": "الإجماليات بعد الفلترة",
    "Saved": "تم الحفظ",
    "No changes recorded in this demo session yet.": "لم تسجل تغييرات في هذه الجلسة حتى الآن.",
    "Payment or stage updated": "تم تعديل الدفعة أو المرحلة",
    "Company identity or opening amounts updated": "تم تعديل بيانات الشركة أو مبالغها الأساسية",
    "Company added": "تمت إضافة شركة",
    "Financial analysis": "التحليل المالي",
    "Activity log": "سجل الحركة",
    "Collection rate": "نسبة التحصيل",
    "Companies": "الشركات",
    "Company": "الشركة",
    "Invoice value": "قيمة الفواتير",
    "Invoice": "الفاتورة",
    "Collected": "المحصل",
    "Receivable": "لصالحنا",
    "Payable": "لصالح الطرف الآخر",
    "Balance": "الرصيد",
    "Direction": "الاتجاه",
    "Progress": "التقدم",
    "Notes": "الملاحظات",
    "Payment": "دفعة",
    "Paid": "المدفوع",
    "Waiting": "انتظار",
    "Prepared": "تم الإعداد",
    "Sent": "تم الإرسال",
    "Settled": "تمت التسوية",
    "Executive view": "الملخص التنفيذي",
    "Unified companies": "الشركات الموحدة",
    "No-show and resolution": "عدم الحضور والحلول",
    "Delivery control": "رقابة التسليم",
    "Operations Control Center": "مركز العمليات",
    "Combined progress": "التقدم المجمع",
    "Receivable variance": "فروقات لصالحنا",
    "Payable variance": "فروقات لصالح الطرف الآخر",
    "Delivered companies": "الشركات المسلمة",
    "Unified company": "الشركة الموحدة",
    "Confidence": "نسبة الثقة",
    "Approved": "معتمد",
    "Needs review": "يحتاج مراجعة",
    "Search ledger": "بحث في سجل الحركة",
    "Movement type": "نوع الحركة",
    "All movements": "كل الحركات",
    "Date": "التاريخ",
    "Time": "الوقت",
    "Project": "المشروع",
    "Action": "الحركة",
    "Before": "قبل",
    "Movement": "الحركة المالية",
    "After": "بعد",
    "No-show bookings": "حجوزات عدم الحضور",
    "Adult": "بالغ",
    "Child": "طفل",
    "Infant": "رضيع",
    "Resolution": "الحل",
    "Open exceptions": "الفروقات المفتوحة",
    "Print or save PDF": "طباعة أو حفظ PDF",
    "Content controls": "إعدادات المحتوى",
    "Report title": "عنوان التقرير",
    "Subtitle": "العنوان الفرعي",
    "Sent from": "مرسل من",
    "Sent to": "مرسل إلى",
    "Prepared by": "إعداد",
    "Print date": "تاريخ الطباعة",
    "Visible identity": "بيانات الهوية الظاهرة",
    "Logos": "الشعارات",
    "Table columns": "أعمدة الجدول",
    "Organization logo": "شعار المؤسسة",
    "Partner logo": "شعار الشريك",
    "Total invoice": "إجمالي الفاتورة",
    "Net balance": "صافي الرصيد",
    "Reviewed by": "مراجعة",
    "Authorized signature and stamp": "التوقيع المعتمد والختم",
    "Report date": "تاريخ التقرير",
    "Invoice Position Statement": "بيان موقف الفواتير",
    "Marine operations finance review": "مراجعة مالية للعمليات البحرية",
    "Finance Operations": "إدارة العمليات المالية",
    "Business Partner": "شريك الأعمال",
    "Accounts Team": "فريق الحسابات",
    "Prepared for reconciliation review and balance confirmation.": "أُعد للمراجعة والمطابقة وتأكيد الرصيد.",
    "Search all source labels...": "ابحث في أسماء المصادر...",
    "Reference, company, service...": "رقم مرجعي، شركة، خدمة...",
    "Reference, trip, hotel, company...": "رقم مرجعي، رحلة، فندق، شركة...",
    "Company, code, notes...": "شركة، كود، ملاحظات...",
    "Reference, company, project, action...": "رقم مرجعي، شركة، مشروع، حركة..."
    ,"Control the report title, parties, preparer, date, notes, logos, metrics, and visible columns before printing. The feature reflects the system's report-building workflow without exposing operational branding.": "تحكم في عنوان التقرير والأطراف والمُعد والتاريخ والملاحظات والشعارات والمؤشرات والأعمدة قبل الطباعة، دون كشف أي علامة تشغيلية حقيقية."
    ,"A live, synthetic showcase of the wider product: combined projects, many-to-many company identity, auditable settlements, no-show valuation, exception resolution, and company delivery.": "عرض تجريبي حي للمنتج الأوسع: مشاريع مجمعة، وربط متعدد لأسماء الشركات، وتسويات قابلة للمراجعة، وتقييم عدم الحضور، وحل الفروقات، وتسليم الشركات."
    ,"Operations control snapshot": "ملخص الرقابة التشغيلية"
    ,"THREE-MONTH BUILD SCOPE": "نطاق تطوير ثلاثة أشهر"
    ,"Operational capabilities represented in the case study": "القدرات التشغيلية المعروضة في دراسة الحالة"
    ,"Documented in the repository": "موثقة داخل المستودع"
    ,"Combined periods with edits preserved in their source projects.": "فترات مجمعة مع بقاء التعديلات مرتبطة بمشاريعها الأصلية."
    ,"Automatic zero-balance resolution and documented agreement outcomes.": "حل تلقائي عند وصول الرصيد إلى صفر أو حل موثق بالاتفاق."
    ,"Amount edits and deletions recorded as auditable financial movements.": "تسجيل تعديلات المبالغ والحذف كحركات مالية قابلة للمراجعة."
    ,"Whole or partial passenger no-shows retained in financial analysis.": "الاحتفاظ بعدم الحضور الكامل أو الجزئي ضمن التحليل المالي."
    ,"Track completed company handovers and produce booking-based statements.": "متابعة تسليم الشركات المكتملة وإصدار كشوف مبنية على الحجوزات."
    ,"Reports and exports use the complete filtered set, not only the visible page.": "التقارير والتصدير يعتمدان كل البيانات المفلترة وليس الصفحة الظاهرة فقط."
    ,"01 / STANDARD RECONCILIATION": "01 / المطابقة العادية"
    ,"Find financial discrepancies before they become reporting problems.": "اكتشف الفروقات المالية قبل أن تتحول إلى مشكلة في التقارير."
    ,"Compare two operational datasets, expose missing and inconsistent records, review company-name mappings, and export an audit-ready exception register.": "قارن مصدرين تشغيليين، واكشف الحجوزات الناقصة وغير المتسقة، وراجع ربط أسماء الشركات، وصدّر سجل فروقات جاهزًا للمراجعة."
    ,"13 booking references, designed to demonstrate every outcome.": "13 رقم حجز مصممة لعرض كل نتائج المطابقة."
    ,"NEW REVIEW": "مراجعة جديدة"
    ,"Upload two source files": "رفع ملفي المصدر"
    ,"Download System A sample": "تحميل نموذج النظام أ"
    ,"Download System B sample": "تحميل نموذج النظام ب"
    ,"Primary operational source": "المصدر التشغيلي الأساسي"
    ,"Counterparty or control source": "مصدر الطرف المقابل أو الرقابة"
    ,"XLSX or CSV, up to 5 MB": "XLSX أو CSV بحد أقصى 5 MB"
    ,"Required columns: Reference, Date, Company, Service, Adult, Child, Infant, Amount.": "الأعمدة المطلوبة: الرقم المرجعي، التاريخ، الشركة، الخدمة، بالغ، طفل، رضيع، المبلغ."
    ,"CONTROL WORKFLOW": "مسار الرقابة"
    ,"From raw records to reviewable exceptions": "من البيانات الخام إلى فروقات قابلة للمراجعة"
    ,"Validate": "تحقق"
    ,"Reject malformed files, missing headers, invalid dates, and non-numeric values.": "ارفض الملفات التالفة والعناوين الناقصة والتواريخ غير الصحيحة والقيم غير الرقمية."
    ,"Normalize": "وحّد"
    ,"Standardize labels and resolve known company aliases before comparison.": "وحّد المسميات واربط الأسماء المعروفة للشركات قبل المقارنة."
    ,"Reconcile": "طابق"
    ,"Compare date, company, service, passenger mix, amount, and record presence.": "قارن التاريخ والشركة والخدمة وتوزيع الركاب والمبلغ ووجود الحجز."
    ,"Review": "راجع"
    ,"Filter discrepancies, inspect mappings, and export an exception register.": "فلتر الفروقات وراجع الربط وصدّر سجل الاستثناءات."
    ,"02 / DETAILED RECONCILIATION": "02 / المطابقة العميقة"
    ,"Audit the booking and the pricing logic behind it.": "راجع الحجز ومنطق التسعير وراءه."
    ,"Compare reference, trip type, hotel or pickup, transfer state, passenger mix, adult rate, calculated amount, and source total without changing the standard workflow.": "قارن الرقم المرجعي ونوع الرحلة والفندق أو نقطة الالتقاء وحالة الترانسفير وتوزيع الركاب وسعر البالغ والمبلغ المحسوب وإجمالي المصدر دون تغيير المسار العادي."
    ,"Includes derived rates, missing transfers, pricing differences, and reference exceptions.": "يشمل الأسعار المشتقة والترانسفير الناقص وفروقات التسعير واستثناءات الرقم المرجعي."
    ,"DETAILED INPUT": "البيانات التفصيلية"
    ,"Upload pricing-level source files": "رفع ملفات المصدر التفصيلية"
    ,"Detailed booking source": "مصدر الحجوزات التفصيلي"
    ,"Detailed comparison source": "مصدر المقارنة التفصيلي"
    ,"Reference, Date, Company, Trip Type, Hotel / Pickup, Adult, Child, Infant, Adult Rate, Amount.": "الرقم المرجعي، التاريخ، الشركة، نوع الرحلة، الفندق أو نقطة الالتقاء، بالغ، طفل، رضيع، سعر البالغ، المبلغ."
    ,"CHARGEABLE PASSENGERS": "الأفراد المحتسبون"
    ,"Adult + (Child x 0.5)": "البالغ + (الطفل × 0.5)"
    ,"INFANT PRICING": "تسعير الرضيع"
    ,"Zero charge": "دون تكلفة"
    ,"MISSING RATE": "السعر غير موجود"
    ,"Amount / chargeable passengers": "المبلغ ÷ الأفراد المحتسبين"
    ,"MISSING AMOUNT": "المبلغ غير موجود"
    ,"Rate x chargeable passengers": "السعر × الأفراد المحتسبين"
    ,"EMPTY PICKUP": "نقطة الالتقاء فارغة"
    ,"03 / INVOICE TRACKING": "03 / متابعة الفواتير"
    ,"Marine operations invoice follow-up": "متابعة فواتير العمليات البحرية"
    ,"Track review, preparation, sending, payment, and the resulting receivable or payable position.": "تابع المراجعة والإعداد والإرسال والدفع وما ينتج عنها من رصيد مستحق أو دائن."
    ,"Invoice tracking views": "تبويبات متابعة الفواتير"
    ,"completed cycles": "دورات مكتملة"
    ,"Synthetic portfolio": "محفظة تجريبية"
    ,"Total entitlement": "إجمالي الاستحقاق"
    ,"Paid plus payment": "المدفوع مع الدفعات"
    ,"Balance due to us": "رصيد مستحق لنا"
    ,"Credit due from us": "رصيد مستحق علينا"
    ,"CYCLE PROGRESS": "تقدم دورة الفاتورة"
    ,"Company completion status": "حالة إنجاز الشركات"
    ,"EXPOSURE": "الموقف المالي"
    ,"Largest open balances": "أكبر الأرصدة المفتوحة"
    ,"RECONCILIATION REVIEW": "مراجعة المطابقة"
    ,"Reconciliation summary": "ملخص المطابقة"
    ,"Field-level differences": "فروقات على مستوى الحقول"
    ,"Repeated reference keys": "أرقام مرجعية مكررة"
    ,"System A minus System B": "النظام أ ناقص النظام ب"
    ,"EXCEPTION REGISTER": "سجل الفروقات"
    ,"None": "لا يوجد"
    ,"Adult count": "عدد البالغين"
    ,"Child count": "عدد الأطفال"
    ,"Infant count": "عدد الرضع"
    ,"Amount": "المبلغ"
    ,"Record availability": "توفر الحجز"
    ,"Service date": "تاريخ الخدمة"
    ,"Service": "الخدمة"
    ,"Company": "الشركة"
    ,"NORMALIZATION CONTROL": "رقابة توحيد البيانات"
    ,"Observed paired references only": "الأرقام المرجعية المقترنة فقط"
    ,"System A label": "اسم النظام أ"
    ,"System B label": "اسم النظام ب"
    ,"Normalized A": "الاسم الموحد أ"
    ,"Normalized B": "الاسم الموحد ب"
    ,"Mapping result": "نتيجة الربط"
    ,"Aligned": "مرتبط"
    ,"Review required": "تحتاج مراجعة"
    ,"DETAILED PRICING REVIEW": "مراجعة التسعير التفصيلية"
    ,"Reference, pricing, pickup, transfer, and passenger controls": "رقابة الرقم المرجعي والتسعير ونقطة الالتقاء والترانسفير والركاب"
    ,"Reference-only control": "رقابة مستقلة بالرقم المرجعي"
    ,"Deep field differences": "فروقات الحقول التفصيلية"
    ,"Across both sources": "عبر المصدرين"
    ,"A minus B": "أ ناقص ب"
    ,"Recorded vs calculated": "المسجل مقابل المحسوب"
    ,"DEEP COMPARISON": "المقارنة العميقة"
    ,"INDEPENDENT KEY": "مفتاح مستقل"
    ,"Matched only by reference": "مطابقة بالرقم المرجعي فقط"
    ,"Trip A / B": "الرحلة أ / ب"
    ,"Hotel or pickup A / B": "الفندق أو نقطة الالتقاء أ / ب"
    ,"Chargeable pax A / B": "الأفراد المحتسبون أ / ب"
    ,"Adult rate A / B": "سعر البالغ أ / ب"
    ,"Amount A / B": "المبلغ أ / ب"
    ,"System A date": "تاريخ النظام أ"
    ,"System B date": "تاريخ النظام ب"
    ,"Trips": "الرحلات"
    ,"A amount": "مبلغ أ"
    ,"B amount": "مبلغ ب"
    ,"CYCLE PROGRESS": "تقدم دورة الفاتورة"
    ,"COMPANY CONTROL": "رقابة الشركات"
    ,"Invoice cycle and balances": "دورة الفاتورة والأرصدة"
    ,"Balance direction": "اتجاه الرصيد"
    ,"All directions": "كل الاتجاهات"
    ,"Code": "الكود"
    ,"Stage": "المرحلة"
    ,"Filtered totals update in the operational system": "تتغير الإجماليات حسب الفلتر في النظام التشغيلي"
    ,"BALANCE DIRECTION": "اتجاه الرصيد"
    ,"Financial exposure": "الموقف المالي"
    ,"STAGE ANALYSIS": "تحليل المراحل"
    ,"Workflow distribution": "توزيع مراحل العمل"
    ,"COMPANY RANKING": "ترتيب الشركات"
    ,"Balances from highest receivable to payable": "الأرصدة من أعلى مستحق لنا إلى المستحق علينا"
    ,"AUDIT TRAIL": "سجل المراجعة"
    ,"Recent financial and workflow movements": "أحدث الحركات المالية والتشغيلية"
    ,"Timestamp": "وقت الحركة"
    ,"Net movement": "صافي الحركة"
    ,"visible": "ظاهر"
    ,"Synthetic marine-tour operations demo": "عرض تجريبي لعمليات الرحلات البحرية"
    ,"Synthetic detailed marine-tour review": "مراجعة تجريبية تفصيلية للرحلات البحرية"
    ,"Hotel / pickup": "الفندق أو نقطة الالتقاء"
    ,"Adult rate": "سعر البالغ"
    ,"ENTERPRISE OPERATIONS LAYER": "طبقة العمليات المؤسسية"
    ,"One synthetic workspace demonstrating multi-project control, company unification, settlements, no-shows, resolution tracking, and invoice delivery.": "مساحة عمل تجريبية واحدة تعرض رقابة المشاريع المجمعة وتوحيد الشركات والتسويات وعدم الحضور ومتابعة الحلول وتسليم الفواتير."
    ,"Across company resolution registers": "عبر سجلات حلول الشركات"
    ,"In our favor": "لصالحنا"
    ,"In partner favor": "لصالح الطرف الآخر"
    ,"Automatic plus agreement": "تلقائي وبالاتفاق"
    ,"Approved booking statements": "كشوف حجوزات معتمدة"
    ,"MULTI-PROJECT CONTROL": "رقابة المشاريع المجمعة"
    ,"Four periods acting as one workspace": "أربع فترات تعمل كمساحة واحدة"
    ,"Source ownership preserved": "مصدر كل سجل محفوظ"
    ,"NET POSITION": "صافي الموقف"
    ,"Financial direction": "الاتجاه المالي"
    ,"Combined net variance": "صافي الفروقات المجمعة"
    ,"Receivable less payable across selected periods": "المستحق لنا ناقص المستحق علينا عبر الفترات المحددة"
    ,"Unify": "وحّد"
    ,"Many labels to one controlled company": "عدة أسماء تحت شركة موحدة"
    ,"Standard and detailed evidence": "أدلة المطابقة العادية والعميقة"
    ,"Resolve": "حل"
    ,"Automatic or documented agreement": "تلقائي أو باتفاق موثق"
    ,"Audit": "راجع"
    ,"Every amount movement remains visible": "كل حركة مبلغ تظل ظاهرة"
    ,"Deliver": "سلّم"
    ,"Approved statement and handover status": "كشف معتمد وحالة تسليم"
    ,"MANY-TO-MANY IDENTITY CONTROL": "رقابة الربط المتعدد للأسماء"
    ,"Unified company groups across projects": "مجموعات الشركات الموحدة عبر المشاريع"
    ,"SEARCH COMPANY OR ALIAS": "بحث باسم الشركة أو الاسم البديل"
    ,"LINK STATUS": "حالة الربط"
    ,"System A labels": "أسماء النظام أ"
    ,"System B labels": "أسماء النظام ب"
    ,"Projects": "المشاريع"
    ,"Aliases": "الأسماء البديلة"
    ,"A group can contain repeated labels from either source and explicit “not present” states without losing the original project relationship.": "يمكن للمجموعة احتواء أسماء مكررة من أي مصدر وحالات غير موجود صريحة دون فقد ارتباطها بالمشروع الأصلي."
    ,"FILTERED MOVEMENT": "الحركة المفلترة"
    ,"Updates with the visible ledger": "تتغير حسب السجل الظاهر"
    ,"AUDIT ENTRIES": "حركات المراجعة"
    ,"Corrections, deletion, and agreement": "تصحيحات وحذف واتفاق"
    ,"PERIODS REPRESENTED": "الفترات الممثلة"
    ,"Original project retained per movement": "المشروع الأصلي محفوظ لكل حركة"
    ,"FINANCIAL AUDIT TRAIL": "سجل المراجعة المالية"
    ,"Settlement movement ledger": "سجل حركات التسوية"
    ,"Settlement movement": "حركة التسويات"
    ,"Amount decreased": "تخفيض مبلغ"
    ,"Amount increased": "زيادة مبلغ"
    ,"Booking deleted": "حذف حجز"
    ,"Agreement resolution": "حل بالاتفاق"
    ,"Visible settlement movement": "إجمالي حركة التسويات الظاهرة"
    ,"Retained in reconciliation totals": "محفوظة ضمن إجماليات المطابقة"
    ,"Adults and children separated": "فصل البالغين والأطفال"
    ,"NO-SHOW CONTROL": "رقابة عدم الحضور"
    ,"Whole and partial booking evidence": "أدلة عدم الحضور الكامل والجزئي"
    ,"SEARCH NO-SHOWS": "بحث في عدم الحضور"
    ,"REVIEW STATUS": "حالة المراجعة"
    ,"Confirmed": "مؤكد"
    ,"Detected shape": "شكل الحالة"
    ,"Value": "القيمة"
    ,"Manual": "يدوي"
    ,"Automatic": "تلقائي"
    ,"Visible no-show value": "قيمة عدم الحضور الظاهرة"
    ,"RESOLUTION REGISTER": "سجل الحلول"
    ,"Automatic zero balance versus documented agreement": "رصيد صفر تلقائي مقابل حل موثق بالاتفاق"
    ,"By agreement": "بالاتفاق"
    ,"Resolved value": "القيمة المحلولة"
    ,"DELIVERED": "تم التسليم"
    ,"Company handovers completed": "تم تسليم الشركات"
    ,"DELIVERED INVOICE VALUE": "قيمة الفواتير المسلمة"
    ,"Based on adjusted System A bookings": "بناءً على حجوزات النظام أ بعد التعديل"
    ,"AWAITING DELIVERY": "بانتظار التسليم"
    ,"Ready and pending companies": "شركات جاهزة وأخرى معلقة"
    ,"COMPANY HANDOVER CONTROL": "رقابة تسليم الشركات"
    ,"Delivery and approved statement readiness": "جاهزية التسليم والكشف المعتمد"
    ,"SEARCH DELIVERY REGISTER": "بحث في سجل التسليم"
    ,"DELIVERY STATUS": "حالة التسليم"
    ,"Delivered": "تم التسليم"
    ,"Ready": "جاهز"
    ,"Pending": "معلق"
    ,"Bookings": "الحجوزات"
    ,"Approved invoice": "الفاتورة المعتمدة"
    ,"Delivered on": "تاريخ التسليم"
    ,"Statement": "الكشف"
    ,"Preview report": "معاينة التقرير"
    ,"Visible approved invoice value": "قيمة الفواتير المعتمدة الظاهرة"
    ,"The operational product generates a company booking statement with configurable identity, notes, signatures, and stamp area through the Report Workshop.": "ينشئ النظام كشف حجوزات للشركة بهوية وملاحظات وتوقيعات ومساحة ختم قابلة للتخصيص من خلال ورشة التقارير."
    ,"Build a professional filtered report by deciding exactly what appears before printing.": "أنشئ تقريرًا احترافيًا مرتبطًا بالفلتر وحدد بدقة ما يظهر قبل الطباعة."
    ,"REPORT IDENTITY": "هوية التقرير"
    ,"Sender": "المرسل"
    ,"Recipient": "المستلم"
    ,"Preparer": "المُعد"
    ,"OPERATIONS": "العمليات"
    ,"FINANCE CONTROL REPORT": "تقرير الرقابة المالية"
    ,"PARTNER": "الشريك"
    ,"STANDARD PROJECTS": "مشاريع المطابقة العادية"
    ,"Monthly reconciliation projects": "مشاريع المطابقة الشهرية"
    ,"Select two or more projects to review them as one workspace": "حدد مشروعين أو أكثر لمراجعتها كمساحة عمل واحدة"
    ,"References": "المراجع"
    ,"Match rate": "نسبة التطابق"
    ,"Variance": "الفرق"
    ,"Open project": "فتح المشروع"
    ,"Open combined workspace": "فتح مساحة المشاريع الموحدة"
    ,"Export combined workbook": "تصدير ملف المشاريع الموحدة"
    ,"DETAILED PROJECTS": "مشاريع المطابقة العميقة"
    ,"Pricing-level reconciliation projects": "مشاريع المطابقة على مستوى التسعير"
    ,"Open several periods without losing each booking's source project": "افتح عدة فترات مع احتفاظ كل حجز بمشروعه الأصلي"
    ,"Back to project library": "العودة إلى قائمة المشاريع"
    ,"STANDARD / COMBINED WORKSPACE": "العادية / مساحة المشاريع الموحدة"
    ,"DETAILED / COMBINED WORKSPACE": "العميقة / مساحة المشاريع الموحدة"
    ,"Projects operating as one reconciliation workspace": "مشاريع تعمل كمساحة مطابقة واحدة"
    ,"Every adjustment remains attached to its original project and booking reference.": "يبقى كل تعديل مرتبطًا بمشروعه الأصلي ومرجع الحجز."
    ,"Open projects": "المشاريع المفتوحة"
    ,"Working together in this view": "تعمل معًا داخل هذا العرض"
    ,"Combined project summary": "ملخص المشاريع الموحدة"
    ,"Rows retain project ownership": "كل صف يحتفظ بالمشروع التابع له"
    ,"Exact matches": "التطابقات الكاملة"
    ,"Recalculated after every edit": "يعاد حسابها بعد كل تعديل"
    ,"Decrease positive, increase negative": "التخفيض موجب والزيادة سالبة"
    ,"Combined bookings": "الحجوزات المجمعة"
    ,"Financial movement ledger": "سجل الحركة المالية"
    ,"LIVE MULTI-PROJECT CONTROL": "رقابة حية متعددة المشاريع"
    ,"Bookings from the selected projects": "حجوزات المشاريع المحددة"
    ,"Project, reference, company, service...": "المشروع أو المرجع أو الشركة أو الخدمة..."
    ,"Amount edits are saved immediately and recorded in the financial movement ledger below.": "تحفظ تعديلات المبالغ فورًا وتسجل في سجل الحركة المالية أدناه."
    ,"Project": "المشروع"
    ,"Save": "حفظ"
    ,"AUDITABLE SETTLEMENTS": "تسويات قابلة للمراجعة"
    ,"Adjustment time": "وقت التعديل"
    ,"Source": "المصدر"
    ,"Before": "قبل"
    ,"After": "بعد"
    ,"Movement": "الحركة"
    ,"Action": "الإجراء"
    ,"Filtered movement total": "إجمالي الحركة بعد الفلترة"
    ,"All sources": "كل المصادر"
    ,"Project, reference, action...": "المشروع أو المرجع أو الإجراء..."
    ,"System A amount adjusted": "تم تعديل مبلغ النظام أ"
    ,"System B amount adjusted": "تم تعديل مبلغ النظام ب"
  };

  const differenceTerms = {
    "Adult count": "عدد البالغين",
    "Child count": "عدد الأطفال",
    "Infant count": "عدد الرضع",
    "Amount": "المبلغ",
    "Record availability": "توفر الحجز",
    "Service date": "تاريخ الخدمة",
    "Service": "الخدمة",
    "Company": "الشركة"
  };

  const normalizedTranslations = Object.fromEntries(
    Object.entries(t).map(([key, value]) => [key.toLocaleLowerCase("en"), value])
  );

  Object.assign(normalizedTranslations, {
    "groups": "مجموعات",
    "movements": "حركات",
    "bookings": "حجوزات",
    "companies": "شركات"
  });

  const patterns = [
    [/^Company name for (.+)$/, "اسم الشركة $1"],
    [/^Invoice total for (.+)$/, "إجمالي فاتورة $1"],
    [/^Paid amount for (.+)$/, "المدفوع لشركة $1"],
    [/^Notes for (.+)$/, "ملاحظات شركة $1"],
    [/^PAYMENT for (.+)$/, "دفعة شركة $1"],
    [/^Stage for (.+)$/, "مرحلة شركة $1"],
    [/^(\d+) exact matches$/, "$1 تطابق كامل"],
    [/^(\d+) A rows \/ (\d+) B rows$/, "$1 صف في أ / $2 صف في ب"],
    [/^(\d+) in A \/ (\d+) in B$/, "$1 في أ / $2 في ب"],
    [/^(\d+) completed cycles$/, "$1 دورات مكتملة"],
    [/^(\d+) visible$/, "$1 ظاهر"],
    [/^Across (\d+) monthly projects$/, "عبر $1 مشاريع شهرية"],
    [/^(\d+) retained bookings$/, "$1 حجوزات محفوظة"],
    [/^(\d+) groups$/, "$1 مجموعات"],
    [/^(\d+) movements$/, "$1 حركات"],
    [/^(\d+) bookings$/, "$1 حجوزات"],
    [/^(\d+) companies$/, "$1 شركات"],
    [/^(\d+) open$/, "$1 مفتوحة"],
    [/^(\d+) companies · (\d+) open exceptions$/, "$1 شركة · $2 فروقات مفتوحة"],
    [/^(\d+) projects selected$/, "$1 مشاريع محددة"],
    [/^([\d,.-]+) movement$/, "$1 حركة"],
    [/^Created (.+) at (.+) UTC$/, "أُنشئت في $1 الساعة $2 بتوقيت UTC"]
  ];

  const translate = (value) => {
    const key = value.trim();
    if (!key) return value;
    let translated = t[key] || normalizedTranslations[key.toLocaleLowerCase("en")];
    if (!translated && key.includes(", ")) {
      const parts = key.split(", ");
      if (parts.every((part) => differenceTerms[part])) translated = parts.map((part) => differenceTerms[part]).join("، ");
    }
    if (!translated) {
      for (const [pattern, replacement] of patterns) {
        if (pattern.test(key)) { translated = key.replace(pattern, replacement); break; }
      }
    }
    if (!translated) return value;
    return `${value.match(/^\s*/)[0]}${translated}${value.match(/\s*$/)[0]}`;
  };

  const translateElement = (root) => {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        return node.nodeValue.trim() && !["SCRIPT", "STYLE"].includes(node.parentElement?.tagName)
          ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => { node.nodeValue = translate(node.nodeValue); });
    root.querySelectorAll?.("[placeholder], [aria-label], [title]").forEach((element) => {
      ["placeholder", "aria-label", "title"].forEach((attribute) => {
        const value = element.getAttribute(attribute);
        if (!value) return;
        const translated = translate(value);
        if (translated !== value) element.setAttribute(attribute, translated.trim());
      });
    });
    root.querySelectorAll?.("input[data-report-input], textarea[data-report-input]").forEach((element) => {
      const translated = translate(element.value);
      if (translated !== element.value) element.value = translated.trim();
    });
  };
  translateElement(document.body);
  window.reconcileflowTranslateElement = translateElement;
  window.reconcileflowTranslateText = (value) => translate(value).trim();
  const titles = {
    "ReconcileFlow | Finance Control Portfolio": "ReconcileFlow | منصة الرقابة المالية",
    "ReconcileFlow | Reconciliation Workspace": "ReconcileFlow | المطابقة العادية",
    "Detailed Reconciliation | ReconcileFlow": "ReconcileFlow | المطابقة العميقة",
    "Invoice Tracking | ReconcileFlow": "ReconcileFlow | متابعة الفواتير",
    "Operations Control Center | ReconcileFlow": "ReconcileFlow | مركز العمليات",
    "Report Workshop | ReconcileFlow": "ReconcileFlow | ورشة التقارير",
    "Combined Projects | ReconcileFlow": "ReconcileFlow | مساحة المشاريع الموحدة"
  };
  document.title = titles[document.title] || document.title;
})();
