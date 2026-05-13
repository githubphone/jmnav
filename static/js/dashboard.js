async function loadDashboard() {
    try {
        var resp = await fetch('/static/data/dashboard.json');
        var data = await resp.json();
        renderFundCharts(data.housing_fund);
        renderHousingCharts(data.affordable_housing);
        renderStatCards(data.housing_fund, data.affordable_housing);
    } catch (e) {
        console.log('Dashboard data not loaded:', e);
    }
}

function renderStatCards(fund, housing) {
    var container = document.getElementById('statCards');
    if (!container) return;
    container.innerHTML = [
        { label: '公积金缴存总额', value: fund.total_deposit + '亿元', color: '#1a3c6e' },
        { label: '公积金提取总额', value: fund.total_withdraw + '亿元', color: '#c0392b' },
        { label: '公积金贷款总额', value: fund.total_loan + '亿元', color: '#2c5aa0' },
        { label: '保障房累计房源', value: housing.total_units + '套', color: '#27ae60' },
    ].map(function (c) {
        return '<div class="stat-card"><div class="stat-value" style="color:' + c.color + '">' + c.value + '</div><div class="stat-label">' + c.label + '</div></div>';
    }).join('');
}

function renderFundCharts(fund) {
    var el = document.getElementById('chartFund');
    if (!el) return;
    var chart = echarts.init(el);
    var years = fund.yearly_summary.map(function (d) { return d.year; });
    chart.setOption({
        title: { text: '公积金年度缴存/提取/贷款趋势', textStyle: { fontSize: 14, color: '#333' } },
        tooltip: { trigger: 'axis' },
        legend: { data: ['缴存额', '提取额', '贷款额'], bottom: 0 },
        grid: { left: 50, right: 20, bottom: 40, top: 40 },
        xAxis: { type: 'category', data: years, axisLabel: { fontSize: 12 } },
        yAxis: { type: 'value', name: '金额（亿元）', nameTextStyle: { fontSize: 11 } },
        series: [
            {
                name: '缴存额', type: 'bar', data: fund.yearly_summary.map(function (d) { return d.deposit; }),
                itemStyle: { color: '#1a3c6e' }, barWidth: 20
            },
            {
                name: '提取额', type: 'bar', data: fund.yearly_summary.map(function (d) { return d.withdraw; }),
                itemStyle: { color: '#c0392b' }, barWidth: 20
            },
            {
                name: '贷款额', type: 'line', data: fund.yearly_summary.map(function (d) { return d.loan; }),
                lineStyle: { color: '#e67e22', width: 3 }, symbol: 'circle', symbolSize: 8,
                itemStyle: { color: '#e67e22' }
            }
        ]
    });
    window.addEventListener('resize', function () { chart.resize(); });
}

function renderHousingCharts(housing) {
    var el1 = document.getElementById('chartHousing');
    if (!el1) return;
    var chart1 = echarts.init(el1);
    var years = housing.yearly.map(function (d) { return d.year; });
    chart1.setOption({
        title: { text: '保障性住房建设与分配情况', textStyle: { fontSize: 14, color: '#333' } },
        tooltip: { trigger: 'axis' },
        legend: { data: ['计划建设', '实际建成', '分配入住'], bottom: 0 },
        grid: { left: 50, right: 20, bottom: 40, top: 40 },
        xAxis: { type: 'category', data: years, axisLabel: { fontSize: 12 } },
        yAxis: { type: 'value', name: '套数', nameTextStyle: { fontSize: 11 } },
        series: [
            {
                name: '计划建设', type: 'bar', data: housing.yearly.map(function (d) { return d.planned; }),
                itemStyle: { color: '#95a5a6' }, barWidth: 18
            },
            {
                name: '实际建成', type: 'bar', data: housing.yearly.map(function (d) { return d.constructed; }),
                itemStyle: { color: '#2980b9' }, barWidth: 18
            },
            {
                name: '分配入住', type: 'bar', data: housing.yearly.map(function (d) { return d.allocated; }),
                itemStyle: { color: '#27ae60' }, barWidth: 18
            }
        ]
    });
    window.addEventListener('resize', function () { chart1.resize(); });

    var el2 = document.getElementById('chartDistrict');
    if (!el2) return;
    var chart2 = echarts.init(el2);
    chart2.setOption({
        title: { text: '各区保障房分配占比', textStyle: { fontSize: 14, color: '#333' }, left: 'center' },
        tooltip: { trigger: 'item', formatter: '{b}: {c}套 ({d}%)' },
        series: [{
            type: 'pie', radius: ['40%', '65%'], center: ['50%', '55%'],
            label: { show: true, formatter: '{b}\n{d}%', fontSize: 11 },
            data: housing.district_distribution.map(function (d) {
                var colors = { '蓬江区': '#1a3c6e', '江海区': '#2c5aa0', '新会区': '#3498db', '台山市': '#27ae60', '开平市': '#e67e22', '鹤山市': '#c0392b', '恩平市': '#95a5a6' };
                return { value: d.count, name: d.district, itemStyle: { color: colors[d.district] || '#999' } };
            })
        }]
    });
    window.addEventListener('resize', function () { chart2.resize(); });
}

document.addEventListener('DOMContentLoaded', loadDashboard);
