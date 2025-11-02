/**
 * 测评报告页面交互逻辑
 */

/**
 * 页面加载时加载报告数据
 */
document.addEventListener('DOMContentLoaded', function() {
    if (window.currentTestId) {
        loadReport();
    }
});

/**
 * 加载报告数据
 */
async function loadReport() {
    try {
        const response = await fetch(`/api/test/${window.currentTestId}`);
        const data = await response.json();
        
        if (data.code === 200) {
            displayReport(data.data);
        } else {
            document.getElementById('report-content').innerHTML = 
                '<div class="error">加载报告失败：' + data.message + '</div>';
        }
    } catch (error) {
        console.error('Error loading report:', error);
        document.getElementById('report-content').innerHTML = 
            '<div class="error">加载报告失败，请稍后重试</div>';
    }
}

/**
 * 显示报告
 */
function displayReport(reportData) {
    const container = document.getElementById('report-content');
    
    const interpretation = reportData.interpretation || {};
    const suggestions = interpretation.suggestions || [];
    
    // 根据等级设置不同的颜色
    const levelColors = {
        'normal': '#28a745',
        'mild': '#ffc107',
        'moderate': '#fd7e14',
        'severe': '#dc3545'
    };
    const levelColor = levelColors[reportData.level_en] || '#667eea';
    
    const suggestionsHtml = suggestions.map(s => `<li>${s}</li>`).join('');
    
    container.innerHTML = `
        <div class="report-header">
            <h2>测评报告</h2>
            <div class="scale-name">${reportData.scale_name}</div>
        </div>
        
        <div class="score-section" style="background: linear-gradient(135deg, ${levelColor} 0%, ${adjustColor(levelColor)} 100%);">
            <div class="score-label">标准分</div>
            <div class="score-value">${reportData.standard_score}</div>
            <div class="level-badge">${reportData.level}</div>
        </div>
        
        <div class="score-details">
            <div class="score-detail-item">
                <div class="label">原始分</div>
                <div class="value">${reportData.raw_score}</div>
            </div>
            <div class="score-detail-item">
                <div class="label">标准分</div>
                <div class="value">${reportData.standard_score}</div>
            </div>
            <div class="score-detail-item">
                <div class="label">测评时长</div>
                <div class="value">${formatDuration(reportData.duration || 0)}</div>
            </div>
            <div class="score-detail-item">
                <div class="label">完成时间</div>
                <div class="value" style="font-size: 1rem;">${formatDate(reportData.completed_at)}</div>
            </div>
        </div>
        
        <div class="interpretation-section">
            <h3>结果解读</h3>
            <div class="interpretation-summary">
                <strong>${interpretation.summary || '测评完成'}</strong>
            </div>
            <div class="interpretation-description">
                ${interpretation.description || '测评已完成，请咨询专业人士解读结果。'}
            </div>
            
            ${suggestions.length > 0 ? `
            <h3 style="margin-top: 2rem;">建议</h3>
            <ul class="suggestions-list">
                ${suggestionsHtml}
            </ul>
            ` : ''}
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ 重要提示</strong>
            本测评结果仅供参考，不能替代专业心理诊断。如果您感到困扰或症状持续，请及时寻求专业心理健康服务。
        </div>
        
        <div class="report-actions">
            <a href="/scales" class="btn btn-primary">返回量表列表</a>
            <button class="btn btn-secondary" onclick="window.print()">打印报告</button>
        </div>
    `;
}

/**
 * 调整颜色（用于渐变）
 */
function adjustColor(color) {
    // 简单的颜色调整，使渐变更明显
    if (color === '#28a745') return '#20c997';
    if (color === '#ffc107') return '#fd7e14';
    if (color === '#fd7e14') return '#dc3545';
    if (color === '#dc3545') return '#c82333';
    return '#764ba2';
}

/**
 * 格式化时长（秒转分:秒）
 */
function formatDuration(seconds) {
    if (!seconds) return '未知';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}分${secs}秒` : `${secs}秒`;
}

/**
 * 格式化日期
 */
function formatDate(dateString) {
    if (!dateString) return '未知';
    // 如果后端返回的已经是格式化字符串，直接使用
    if (dateString.includes('-') && dateString.includes(' ')) {
        return dateString;
    }
    // 否则尝试解析ISO格式
    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return dateString;
        }
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    } catch (e) {
        return dateString;
    }
}

