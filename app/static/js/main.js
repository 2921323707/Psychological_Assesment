/**
 * 主JavaScript文件
 */

// 全局工具函数
const Utils = {
    /**
     * 格式化日期
     */
    formatDate(date) {
        if (!date) return '';
        const d = new Date(date);
        return d.toLocaleDateString('zh-CN');
    },

    /**
     * API请求封装
     */
    async fetchAPI(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    },

    /**
     * 显示消息提示
     */
    showMessage(message, type = 'info') {
        // 简单的alert实现，后续可以替换为更美观的提示组件
        alert(message);
    },

    /**
     * 滚动到顶部
     */
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
};

// 导出到全局
window.Utils = Utils;

console.log('心理测评系统已加载');

