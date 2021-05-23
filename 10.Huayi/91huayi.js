// ==UserScript==
// @name         华医网自动播放与答题
// @namespace    http://tampermonkey.net/
// @version      0.4
// @description  打开视频播放页面后即可自动完成所有课程
// @author       砖瓦核弹头&肖翔
// @match        *://*.91huayi.com/course_ware/course_ware_polyv.aspx?*
// @match        *://*.91huayi.com/pages/exam.aspx?*
// @match        *://*.91huayi.com/pages/exam_result.aspx?*
// @match        *://*.91huayi.com/*
// @match        *://jsxx.gdedu.gov.cn/groupIndex/goStudentActPage.do?*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    var keyTest = "jixujiaoyuTest";
    var keyResult = "jixujiaoyuResult";
    var urlInfos = window.location.href.split("/");
    var urlTip = urlInfos[urlInfos.length - 1].split("?")[0];
    var huayi = getHuayi();

    if (urlTip == "course_ware_polyv.aspx") { //视频页面
        console.log("当前任务: 华医看视频")
        huayi.seeVideo()
    } else if (urlTip == "exam.aspx") { //考试页面
        console.log("当前任务: 华医考试")
        huayi.doTest()
    } else if (urlTip == "exam_result.aspx") { //考试结果页面
        console.log("当前任务: 华医考试结果审核")
        huayi.doResult()
    } else if (urlTip == "goStudentActPage.do") {
        console.log("当前任务: 教师公需课 ")
        getTeacher().dealProblem()
    } else {
        console.log("其它")
    }


    function getHuayi() {




        return {
            seeVideo: function () {
                localStorage.removeItem(keyTest);
                localStorage.removeItem(keyResult);
				checkHuaYiQuestion();
               // var myid = prefix + vid;
                var myinter = setInterval(function () {
                    var myvideo =  document.querySelector("video");
                    console.log("当前进度: " + myvideo.currentTime + " 总进度: " + myvideo.duration);
                    if (myvideo.currentTime == myvideo.duration) {
                        window.clearInterval(myinter);
                        setTimeout(function () {
                            check_next_click();
                        }, 1000);
                        //console.log("三秒后进入下一步");
                    }
                }, 3000);

                window.s2j_onPlayOver = function () {
                    console.log("播放完毕")
                    showExam(true);
                    delCookie("playState");
                    addCourseWarePlayRecord();
                    setTimeout(function () {
                        document.querySelector(".inputstyle2").click()
                    }, 1000)
                }
            },
            doTest: function () {
                var questions = {};
                var index = 0;
                var oldTest = JSON.parse(localStorage.getItem(keyTest));
                var w = localStorage.getItem(keyResult);
                var wrongs = w ? w.split("&") : null;
                while (true) {
                    var question = document.querySelector("#gvQuestion_question_" + index);
                    if (question == null) break;
                    else {
                        var q = question.innerHTML.substring(2);
                        questions[q] = "A";
                        if (oldTest && oldTest[q]) {
                            questions[q] = oldTest[q];
                        }
                        if (wrongs && wrongs.indexOf(q) != -1) { //旧选项错误
                            console.log("旧选项错误   " + q);
                            questions[q] = getNextChoice(questions[q]);
                        }
                        var answer = getChoiceCode(questions[q]);
                        var element = document.querySelector("#gvQuestion_rbl_" + index + "_" + answer + "_" + index);
                        if (!element) {
                            console.log("找不到选项，默认选A index: " + index + " answer: " + answer);
                            questions[q] = "A";
                            answer = getChoiceCode("A");
                            element = document.querySelector("#gvQuestion_rbl_" + index + "_" + answer + "_" + index);
                            //localStorage.removeItem(keyTest)
                        }
                        element.click();
                        index = index + 1;
                    }
                }
                console.log(questions)

                localStorage.setItem(keyTest, JSON.stringify(questions));

                setTimeout(function () {
                    document.querySelector("#btn_submit").click();
                }, 1000);

                function getChoiceCode(an) { //用于获取选项字符编码
                    return an.charCodeAt(0) - "A".charCodeAt(0);
                }

                function getNextChoice(an) { //用于获取下一个选项字符
                    var code = an.charCodeAt(0) + 1;
                    return String.fromCharCode(code);
                }
            },
            doResult: function () {
                var res = document.getElementsByTagName("b")[0].innerText;
                var dds = document.getElementsByTagName("dd");
                if (res == "考试通过！") { //考试通过
                    console.log("考试通过")
                    var next = document.querySelector(".two");
                    if (next) {
                        next.click();
                    }
                } else { //考试没过
                    console.log("考试未通过")
                    var wrong = "";
                    for (var i = 0; i < dds.length; ++i) {
                        wrong = wrong + dds[i].title + "&";
                    }
                    console.log(wrong)
                    if (wrong.length != 0) {
                        localStorage.setItem(keyResult, wrong);
                        document.querySelector(".button").getElementsByTagName("input")[1].click(); //重新考试
                    }
                }

            }
        }
    }

    function getTeacher() {
        return {
            dealProblem: function () {
                localStorage.removeItem(keyTest)
                localStorage.removeItem(keyResult)
                finishTecher()

                function finishTecher() {
                    var res = document.querySelector("#actName").innerText.indexOf("课程考核")
                    if (res != -1) { //课程考核
                        console.log("课程考核")
                        dealQuestions()
                    } else {
                        console.log("看视频")
                        var work = setInterval(function () {
                            if (player && player.isPlaying) {
                                var duration = player.getDuration(); // 显示总时长
                                var position = player.getPosition(); // 视频当前时间
                                if (dyna_pro_over != 'Y' && position != null && position != '0' && position != '' && position != undefined && typeof (position) != 'undefined' && duration != null && duration != '0' && duration != '' && duration != undefined && typeof (duration) != 'undefined' && position > 0) {
                                    //如果触发这个操作后，标识已经完成完成
                                    setDyna(videoId, 'ACT007', 'Y', 'Y', position, '0', '0');
                                    //设置页面的是否完成的标识
                                    $('#dyna_pro_over').val('Y');
                                }
                                window.clearInterval(work)
                                console.log("当前视频完成")
                                freshNowVideoFinishState() //更新当前视频的完成标志
                                var next = getNextVideo()
                                if (next) {
                                    next.click()
                                    finishTecher()
                                } else {
                                    player.seek(Math.floor(player.getDuration()))
                                    alert("所有视频观看完毕")
                                }
                            }
                        }, 10000)
                    }

                }

                function freshNowVideoFinishState() {
                    document.querySelector(".data.cur").childNodes[1].firstElementChild.setAttribute("src", "http://jsxxcss.gdedu.gov.cn/profession_lecture/latest/images/round_full.png")
                }

                function getNextVideo() {
                    var imgs = document.getElementsByTagName("img")
                    for (var i = 0; i < imgs.length; ++i) {
                        if (imgs[i].src == "http://jsxxcss.gdedu.gov.cn/profession_lecture/latest/images/round_empty.png" || imgs[i].src == "http://jsxxcss.gdedu.gov.cn/profession_lecture/latest/images/round_half.png") { //未完成节点
                            return imgs[i].parentElement.parentElement
                        }
                    }
                    return null
                }

                function dealQuestions() {
                    var qs = document.getElementsByClassName("oh")
                    var questions = {}
                    var oldQuestions = JSON.parse(localStorage.getItem(keyTest))
                    var wrongs = JSON.parse(localStorage.getItem(keyResult))
                    for (var i = 0; i < qs.length; ++i) {
                        var q = qs[i].firstElementChild.firstElementChild.firstElementChild.innerText.substring(2)
                        questions[q] = "A"
                        if (wrongs && wrongs[q]) {
                            //console.log(q)
                            questions[q] = wrongs[q]
                        }
                        var cs = questions[q].split(",")
                        for (var j = 0; j < cs.length; ++j) {
                            if (cs[j]) {
                                var code = getChoiceCode(cs[j])
                                var choice = qs[i].children[1].children[code]
                                if (choice) {
                                    choice.firstElementChild.firstElementChild.firstElementChild.click()
                                } else {
                                    console.log("i: " + i + " code: " + code + " cs[j]: " + cs[j])
                                }
                            }
                        }

                    }
                    localStorage.setItem(keyTest, JSON.stringify(questions))
                    setTimeout(function () {
                        document.querySelector("#submitBtn").click()
                        var work2 = setInterval(function () {
                            if (!document.querySelector("#submitBtn")) {
                                window.clearInterval(work2)
                                doResult()
                            }
                        }, 1000)
                    }, 1000)

                }

                function getChoiceCode(an) { //用于获取选项字符编码
                    return an.charCodeAt(0) - "A".charCodeAt(0);
                }

                function doResult() {
                    console.log("获取正确答案")
                    if (document.querySelector(".fr").parentElement.innerText.match(/\d+分/)[0] == "100分") {
                        alert("已经满分了，可以关闭此网页了")
                        return
                    }
                    var qs = document.getElementsByClassName("oh")
                    var wrongs = JSON.parse(localStorage.getItem(keyResult))
                    if (!wrongs) wrongs = {}
                    for (var i = 0; i < qs.length; ++i) {
                        var cs = qs[i].children[1].children
                        var q = qs[i].firstElementChild.firstElementChild.firstElementChild.innerText.substring(2)
                        if (wrongs[q]) wrongs[q] = ""
                        for (var j = 0; j < cs.length; ++j) {
                            if (cs[j] && cs[j].firstElementChild.lastElementChild.getAttribute("class") == "right-answer") {
                                wrongs[q] = wrongs[q] + "," + String.fromCharCode("A".charCodeAt(0) + j);
                            }
                        }
                    }
                    localStorage.setItem(keyResult, JSON.stringify(wrongs))
                    setTimeout(function () {
                        document.querySelector(".redoBtn").click()
                        var work3 = setInterval(function () {
                            if (document.querySelector("#submitBtn")) {
                                window.clearInterval(work3)
                                dealQuestions()
                            }
                        }, 1000)
                    }, 1000)

                }
            }
        }
    }

	function checkHuaYiQuestion(){
		setInterval(
			function() {
				console.log("检查课堂问答")
				var submitBtn=document.querySelectorAll("div[class='pv-ask-foot']")[0];
				var skipBtn = document.querySelectorAll("div[class='pv-ask-foot']")[1];

				//判断是否有题目，没有题目跳过所有:
				if(submitBtn.innerText=="提交"){
					var 	totalOptionNums=document.querySelectorAll("div[class='pv-ask-form']").length;
					//是否有cookies
					//没有 创建并设置答题备选数cookies为选项个数
					//有 读取答题备选数cookies
					var canSelectNums=getCookie("canSelectNums").length==0? setCookie("canSelectNums", totalOptionNums):getCookie("canSelectNums")
					//点击选项  索引为 选项数-答题备选数
					document.querySelectorAll("div[class='pv-ask-form']")[totalOptionNums-canSelectNums].querySelector("input").click();
					submitBtn.querySelector("button").click();
					var answerResultBtn = document.querySelectorAll("div[class='pv-ask-foot']")[1].querySelector("button[class='pv-ask-default']");
					//回答正确->答题备选数cookies删除，点击提交按钮，setTime点击关闭按钮
					if(answerResultBtn.innerText=="关闭"){
						delCookie("canSelectNums");
						setTimeout(function () {
							answerResultBtn.click();
	                            }, 3000);

					}
					//回答错误->答题备选数cookies-1，点击再看一次按钮
					if(answerResultBtn.innerText=="再看一次"){

						setCookie("canSelectNums", canSelectNums-1);
						setTimeout(function () {
							answerResultBtn.click();
	                            }, 3000)
					}


				}
				else{
					//不答题，跳过题目:
					try{
						skipBtn.querySelector("button").click();
					}
					catch(e){
						console.log(e)
					}
				}
			}
		,5000)
    }
	//工具函数
		function delCookie(name) {
					var exp = new Date();
					exp.setTime(exp.getTime() - 1);
					var cval = getCookie(name);
					if (cval != null)
						document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
			}


		function setCookie(name, value) {
			document.cookie = name + '=' + value;
		}

		function getCookie(name) {
			var arr = document.cookie.split('; ');
			for (var i = 0; i < arr.length; i++) {
				var arr2 = arr[i].split('=');
				if (arr2[0] == name) {
					return arr2[1];
				}
			}
			return '';
		}

    // Your code here...
})();
