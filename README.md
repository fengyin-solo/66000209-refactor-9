# solo-6600020: Modbus 工业协议数据采集监控大屏

## 技术栈
- Frontend: Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS + ECharts
- Backend: Python FastAPI + pymodbus

## 核心特性
1. **Modbus RTU/TCP 寄存器实时读取**：pymodbus 连接工业设备
2. **时序曲线 ECharts 绘制**：实时趋势图，多寄存器对比
3. **阈值告警 WebSocket 推送**：温度/压力超限自动告警
4. **设备拓扑 SVG 图**：可视化设备布局与在线状态
5. **采集任务调度**：可调轮询间隔，设备启停控制

## 设备与点位定义
`shared/devices.json` 是设备与点位（寄存器）默认定义的唯一来源，后端 API 与前端页面都从这里加载。
新增/修改设备数量、点位名称、单位、初始值只需改这一个文件，设备列表接口与实时读取会自动保持一致。

## 启动
```bash
cd frontend && npm install && npm run dev
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8002
```
