var ec_right2 = echarts.init(document.getElementById("r2"), "dark")

var ec_right2_option = {
    title: {
        text: '全国治愈死亡情况',
        left: 'center',
        top: 20,
        textStyle: {
            color: 'white'
        }
    },
    tooltip: {
        trigger: 'axis'
    },
    visualMap: {
        show: false,
        min: 280000,
        max: 4800000,
        inRange: {
            colorLightness: [0, 1]
        }
    },
    series: [
        {
            name: 'Access From',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: [
                {value: 310, name: '治愈'},
                {value: 274, name: '现存确诊'},
                {value: 235, name: '累计确诊'}
            ].sort(function (a, b) {
                return a.value - b.value;
            }),
            roseType: 'radius',
            label: {
                color: 'rgba(255, 255, 255, 0.3)'
            },
            labelLine: {
                lineStyle: {
                    color: 'rgba(255, 255, 255, 0.3)'
                },
                smooth: 0.2,
                length: 10,
                length2: 20
            },
            itemStyle: {
                color: '#c23531',
                shadowBlur: 200,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            },
            animationType: 'scale',
            animationEasing: 'elasticOut',
            animationDelay: function (idx) {
                return Math.random() * 200;
            }
        }
    ]
};

ec_right2.setOption(ec_right2_option)