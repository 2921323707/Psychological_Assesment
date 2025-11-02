/**
 * 测评页面交互逻辑
 */

let scaleData = null;
let scaleItems = [];
let currentQuestionIndex = 0;
let answers = {}; // 存储答案 {itemId: selectedValue}
let startTime = null;

/**
 * 页面加载时初始化
 */
document.addEventListener('DOMContentLoaded', function() {
    if (window.currentScaleId) {
        loadScaleData();
    }
});

/**
 * 加载量表数据
 */
async function loadScaleData() {
    try {
        // 加载量表详情
        const detailResponse = await fetch(`/api/scales/${window.currentScaleId}`);
        const detailData = await detailResponse.json();
        
        if (detailData.code === 200) {
            scaleData = detailData.data;
            displayIntro();
        } else {
            alert('加载量表信息失败');
            window.location.href = '/scales';
        }
        
        // 加载题目列表
        const itemsResponse = await fetch(`/api/scales/${window.currentScaleId}/items`);
        const itemsData = await itemsResponse.json();
        
        if (itemsData.code === 200) {
            scaleItems = itemsData.data.items;
            // 从localStorage恢复答案（如果有）
            loadAnswersFromStorage();
        } else {
            alert('加载题目失败');
        }
    } catch (error) {
        console.error('Error loading scale data:', error);
        alert('加载数据失败，请稍后重试');
        window.location.href = '/scales';
    }
}

/**
 * 显示测评说明页
 */
function displayIntro() {
    document.getElementById('scale-name').textContent = scaleData.name;
    document.getElementById('scale-description').textContent = scaleData.description || '暂无描述';
    document.getElementById('scale-instruction').textContent = scaleData.instruction || '请根据最近一周的情况，选择最符合您的选项';
    
    // 估算时间
    const estimatedMinutes = Math.ceil(scaleData.total_items * 0.5);
    document.getElementById('estimated-time').textContent = estimatedMinutes;
}

/**
 * 开始测评
 */
function startTest() {
    if (!scaleItems || scaleItems.length === 0) {
        alert('题目数据未加载完成，请稍后重试');
        return;
    }
    
    document.getElementById('test-intro').style.display = 'none';
    document.getElementById('test-page').style.display = 'block';
    
    startTime = Date.now();
    currentQuestionIndex = 0;
    displayQuestion();
    
    // 页面可见性变化时保存答案
    document.addEventListener('visibilitychange', saveAnswersToStorage);
    // 页面卸载前保存答案
    window.addEventListener('beforeunload', saveAnswersToStorage);
}

/**
 * 显示当前题目
 */
function displayQuestion() {
    if (currentQuestionIndex >= scaleItems.length) {
        submitTest();
        return;
    }
    
    const item = scaleItems[currentQuestionIndex];
    const questionNum = currentQuestionIndex + 1;
    
    // 更新题目编号和文本
    document.getElementById('question-number').textContent = questionNum;
    document.getElementById('current-question-num').textContent = questionNum;
    document.getElementById('total-questions').textContent = scaleItems.length;
    document.getElementById('question-text').textContent = item.question;
    
    // 更新进度
    const progress = (questionNum / scaleItems.length) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';
    document.getElementById('progress-percent').textContent = Math.round(progress) + '%';
    
    // 显示选项
    displayOptions(item);
    
    // 更新导航按钮
    updateNavButtons();
    
    // 恢复已保存的答案
    restoreAnswer(item.id);
}

/**
 * 显示选项
 */
function displayOptions(item) {
    const optionsList = document.getElementById('options-list');
    optionsList.innerHTML = '';
    
    if (!item.options || item.options.length === 0) {
        optionsList.innerHTML = '<p>题目选项加载失败</p>';
        return;
    }
    
    item.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option-item';
        optionDiv.onclick = () => selectOption(item.id, option.value, optionDiv);
        
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = `question_${item.id}`;
        radio.value = option.value;
        radio.id = `option_${item.id}_${index}`;
        
        const label = document.createElement('label');
        label.htmlFor = `option_${item.id}_${index}`;
        label.textContent = option.text;
        
        optionDiv.appendChild(radio);
        optionDiv.appendChild(label);
        optionsList.appendChild(optionDiv);
    });
}

/**
 * 选择选项
 */
function selectOption(itemId, value, optionDiv) {
    // 移除其他选项的选中状态
    const options = document.querySelectorAll(`input[name="question_${itemId}"]`);
    options.forEach(opt => {
        opt.checked = false;
        opt.closest('.option-item').classList.remove('selected');
    });
    
    // 设置当前选项为选中
    const radio = optionDiv.querySelector('input[type="radio"]');
    if (radio) {
        radio.checked = true;
        optionDiv.classList.add('selected');
        answers[itemId] = value;
        saveAnswersToStorage();
    }
    
    // 更新导航按钮状态
    updateNavButtons();
}

/**
 * 恢复答案
 */
function restoreAnswer(itemId) {
    const savedAnswer = answers[itemId];
    if (savedAnswer !== undefined) {
        const radio = document.querySelector(`input[name="question_${itemId}"][value="${savedAnswer}"]`);
        if (radio) {
            radio.checked = true;
            radio.closest('.option-item').classList.add('selected');
        }
    }
}

/**
 * 更新导航按钮
 */
function updateNavButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    
    // 上一题按钮
    prevBtn.disabled = currentQuestionIndex === 0;
    
    // 下一题/提交按钮
    const hasAnswer = answers[scaleItems[currentQuestionIndex]?.id] !== undefined;
    
    if (currentQuestionIndex === scaleItems.length - 1) {
        // 最后一题
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'inline-block';
        submitBtn.disabled = !hasAnswer;
    } else {
        nextBtn.style.display = 'inline-block';
        submitBtn.style.display = 'none';
        nextBtn.disabled = !hasAnswer;
    }
}

/**
 * 上一题
 */
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

/**
 * 下一题
 */
function nextQuestion() {
    const currentItem = scaleItems[currentQuestionIndex];
    if (!answers[currentItem.id]) {
        alert('请选择答案后再继续');
        return;
    }
    
    if (currentQuestionIndex < scaleItems.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
}

/**
 * 提交测试
 */
function submitTest() {
    // 检查是否有未答题
    const unanswered = [];
    scaleItems.forEach(item => {
        if (answers[item.id] === undefined) {
            unanswered.push(item.order);
        }
    });
    
    if (unanswered.length > 0) {
        document.getElementById('unanswered-count').textContent = unanswered.length;
        document.getElementById('submit-modal').style.display = 'flex';
        return;
    }
    
    // 所有题目都已作答，直接提交
    confirmSubmit();
}

/**
 * 关闭提交确认对话框
 */
function closeSubmitModal() {
    document.getElementById('submit-modal').style.display = 'none';
}

/**
 * 确认提交
 */
async function confirmSubmit() {
    closeSubmitModal();
    
    // 计算测试时长
    const duration = startTime ? Math.round((Date.now() - startTime) / 1000) : 0;
    
    // 准备提交数据
    const submitData = {
        scale_id: parseInt(window.currentScaleId),
        answers: answers,
        duration: duration
    };
    
    try {
        const response = await fetch('/api/test/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(submitData)
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
            // 清除本地存储的答案
            localStorage.removeItem(`test_answers_${window.currentScaleId}`);
            
            // 跳转到报告页面
            window.location.href = `/report?test_id=${result.data.test_id}`;
        } else {
            alert('提交失败：' + result.message);
        }
    } catch (error) {
        console.error('Error submitting test:', error);
        alert('提交失败，请稍后重试');
    }
}

/**
 * 保存答案到localStorage
 */
function saveAnswersToStorage() {
    if (window.currentScaleId && Object.keys(answers).length > 0) {
        localStorage.setItem(`test_answers_${window.currentScaleId}`, JSON.stringify(answers));
        localStorage.setItem(`test_current_index_${window.currentScaleId}`, currentQuestionIndex.toString());
    }
}

/**
 * 从localStorage加载答案
 */
function loadAnswersFromStorage() {
    if (window.currentScaleId) {
        const saved = localStorage.getItem(`test_answers_${window.currentScaleId}`);
        const savedIndex = localStorage.getItem(`test_current_index_${window.currentScaleId}`);
        
        if (saved) {
            answers = JSON.parse(saved);
        }
        
        if (savedIndex && parseInt(savedIndex) > 0) {
            // 询问是否继续之前的测试
            const continueTest = confirm('检测到您有未完成的测试，是否继续？');
            if (continueTest) {
                currentQuestionIndex = parseInt(savedIndex);
                // 如果正在测评页面，直接显示题目
                if (document.getElementById('test-page').style.display !== 'none') {
                    displayQuestion();
                }
            } else {
                // 清除保存的答案
                localStorage.removeItem(`test_answers_${window.currentScaleId}`);
                localStorage.removeItem(`test_current_index_${window.currentScaleId}`);
                answers = {};
            }
        }
    }
}

// 导出函数供HTML调用
window.startTest = startTest;
window.previousQuestion = previousQuestion;
window.nextQuestion = nextQuestion;
window.submitTest = submitTest;
window.closeSubmitModal = closeSubmitModal;
window.confirmSubmit = confirmSubmit;

