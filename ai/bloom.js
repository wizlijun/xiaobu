document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('graph-container');
    const svg = document.getElementById('lines-svg');

    // --- Knowledge Card Data ---
    // Positions are approximate and may need adjustment.
    // content can include HTML for facts and opinions
    const cardsData = [
        {
            id: 'revised_bloom', title: '核心理念: 修订版布鲁姆教育目标分类学',
            content: `基于原布鲁姆分类学，<span class="emphasis">旨在帮助教师理解和实施基于标准的课程</span>。<br>
                      由Lorin Anderson和David Krathwohl等认知心理学家、课程专家、教师教育者和研究者共同开发。<br>
                      <span class="opinion">观点: 这是一个更实用、更符合当前教育认知和实践的框架。</span>`,
            x: 550, y: 50, connections: ['taxonomy_table', 'two_dimensions', 'purpose', 'changes_from_original']
        },
        {
            id: 'taxonomy_table', title: '核心结构: 分类学表 (The Taxonomy Table)',
            content: `一个<span class="fact">二维框架</span> (行和列)。<br>
                      - 行: <span class="emphasis">知识维度</span> (Knowledge Dimension)<br>
                      - 列: <span class="emphasis">认知过程维度</span> (Cognitive Process Dimension)<br>
                      单元格代表知识与认知过程的特定交叉点，用于对教育目标进行分类。<br>
                      <span class="opinion">强调: 该表是分析和规划教学、学习与评估的中心工具。</span>`,
            x: 550, y: 250, type: 'structure', connections: ['knowledge_dimension_summary', 'cognitive_process_summary']
        },
        {
            id: 'two_dimensions', title: '两大维度',
            content: `分类学表由两个相互独立的维度构成。<br>
                      <span class="fact">事实: 这是对原布鲁姆分类学中知识和认知过程分离和重组的结果。</span>`,
            x: 300, y: 250, type: 'structure', connections: ['knowledge_dimension_summary', 'cognitive_process_summary']
        },
        {
            id: 'knowledge_dimension_summary', title: '知识维度 (Knowledge Dimension)',
            content: `描述学生预期学习的<span class="emphasis">内容类型</span>。<br>
                      <span class="fact">包含四种主要类型:</span>
                      <ul>
                        <li>事实性知识 (Factual)</li>
                        <li>概念性知识 (Conceptual)</li>
                        <li>程序性知识 (Procedural)</li>
                        <li>元认知知识 (Metacognitive)</li>
                      </ul>
                      <span class="opinion">强调: 元认知知识的加入是重要的修订。</span>`,
            x: 150, y: 450, type: 'knowledge', connections: ['factual_knowledge', 'conceptual_knowledge', 'procedural_knowledge', 'metacognitive_knowledge']
        },
        {
            id: 'cognitive_process_summary', title: '认知过程维度 (Cognitive Process Dimension)',
            content: `描述学生在学习和运用知识时所进行的<span class="emphasis">思维活动类型</span>。<br>
                      <span class="fact">包含六个主要类别 (动词形式):</span>
                      <ul>
                        <li>记忆 (Remember)</li>
                        <li>理解 (Understand)</li>
                        <li>应用 (Apply)</li>
                        <li>分析 (Analyze)</li>
                        <li>评价 (Evaluate)</li>
                        <li>创造 (Create)</li>
                      </ul>
                      <span class="opinion">强调: 认知过程类别被认为是按复杂性递增排列，但并非严格的累积层级。创造被视为最复杂的过程。</span>`,
            x: 450, y: 450, type: 'process', connections: ['remember_cp', 'understand_cp', 'apply_cp', 'analyze_cp', 'evaluate_cp', 'create_cp']
        },
        {
            id: 'purpose', title: '修订目的与用途',
            content: `1. <span class="emphasis">整合新知识</span>：融入近几十年认知心理学和教育研究的成果。<br>
                      2. <span class="emphasis">提升实用性</span>：为教师提供更清晰、更易用的工具。<br>
                      3. <span class="emphasis">促进对齐</span>：帮助教育者确保学习目标、教学活动和评估方法的一致性 (Alignment)。<br>
                      <span class="opinion">观点: 修订版旨在成为教育者规划、实施和评估学生学习的强制性参考。</span>`,
            x: 850, y: 250, type: 'application', connections: ['alignment']
        },
        {
            id: 'alignment', title: '对齐 (Alignment)',
            content: `<span class="fact">指教育目标、教学活动和评估方法之间的一致性程度。</span><br>
                      <span class="opinion">强调: 分类学表是检查和促进“对齐”的有力工具，对齐是有效教学的关键。</span>`,
            x: 850, y: 450, type: 'application'
        },
        {
            id: 'changes_from_original', title: '与原版布鲁姆分类学的主要区别',
            content: `<ul>
                        <li><span class="fact">结构变化</span>: 从一维变为二维 (知识维度和认知过程维度)。</li>
                        <li><span class="fact">术语变化</span>: 认知过程类别使用动词形式；原“知识”类别成为“记忆”；原“综合”变为“创造”；原“理解”(Comprehension) 变为“理解”(Understand)。</li>
                        <li><span class="fact">知识维度细化</span>: 明确区分事实性、概念性、程序性知识，并<span class="emphasis">新增元认知知识</span>。</li>
                        <li><span class="fact">层级关系</span>: 认知过程维度强调复杂性增加，但<span class="opinion">不再是严格的累积层级</span>；“创造”位于最高层。</li>
                        <li><span class="emphasis">应用焦点</span>: 更强调在课程、教学和评估中的实际应用。</li>
                      </ul>`,
            x: 1050, y: 200, type: 'change'
        },
        // Detailed cards for Knowledge Dimension
        {
            id: 'factual_knowledge', title: '事实性知识 (Factual)',
            content: `学生必须知道的基本元素或信息的孤立片段。<br>
                      - Aa. <span class="emphasis">术语知识</span><br>
                      - Ab. <span class="emphasis">具体细节和元素的知识</span>`,
            x: 50, y: 600, type: 'knowledge'
        },
        {
            id: 'conceptual_knowledge', title: '概念性知识 (Conceptual)',
            content: `更复杂、更有组织的知识形式，元素之间的内在联系。<br>
                      - Ba. <span class="emphasis">分类和类别的知识</span><br>
                      - Bb. <span class="emphasis">原理和通则的知识</span><br>
                      - Bc. <span class="emphasis">理论、模型和结构的知识</span>`,
            x: 150, y: 700, type: 'knowledge'
        },
        {
            id: 'procedural_knowledge', title: '程序性知识 (Procedural)',
            content: `如何做某事、探究方法、使用技能/算法/技术的标准。<br>
                      - Ca. <span class="emphasis">特定学科技能和算法的知识</span><br>
                      - Cb. <span class="emphasis">特定学科技术和方法的知识</span><br>
                      - Cc. <span class="emphasis">确定何时使用适当程序的标准知识</span>`,
            x: 250, y: 600, type: 'knowledge'
        },
        {
            id: 'metacognitive_knowledge', title: '元认知知识 (Metacognitive)',
            content: `关于一般认知以及个体自身认知的意识和知识。<span class="fact">这是修订版新增的重要类别。</span><br>
                      - Da. <span class="emphasis">策略知识</span><br>
                      - Db. <span class="emphasis">关于认知任务的知识</span> (包括情境和条件知识)<br>
                      - Dc. <span class="emphasis">自我知识</span>`,
            x: 350, y: 700, type: 'knowledge'
        },
         // Detailed cards for Cognitive Process Dimension
        {id: 'remember_cp', title: '记忆 (Remember)', content: `从长时记忆中提取相关知识。包括<span class="emphasis">识别</span>和<span class="emphasis">回忆</span>。`, x: 400, y: 600, type: 'process'},
        {id: 'understand_cp', title: '理解 (Understand)', content: `建构教学信息的意义。包括<span class="emphasis">解释、举例、分类、总结、推断、比较、说明</span>。`, x: 500, y: 700, type: 'process'},
        {id: 'apply_cp', title: '应用 (Apply)', content: `在给定情境中执行或使用程序。包括<span class="emphasis">执行</span>和<span class="emphasis">实施</span>。`, x: 600, y: 600, type: 'process'},
        {id: 'analyze_cp', title: '分析 (Analyze)', content: `将材料分解为其组成部分，并确定各部分之间以及与整体结构或目的的关系。包括<span class="emphasis">区分、组织、归因</span>。`, x: 700, y: 700, type: 'process'},
        {id: 'evaluate_cp', title: '评价 (Evaluate)', content: `依据标准和准则做出判断。包括<span class="emphasis">检查</span>和<span class="emphasis">批判</span>。`, x: 800, y: 600, type: 'process'},
        {id: 'create_cp', title: '创造 (Create)', content: `将元素整合形成一个连贯或功能性的整体；将元素重组为新的模式或结构。包括<span class="emphasis">生成、规划、制作</span>。<span class="fact">这是认知过程维度中最高层次的活动。</span>`, x: 900, y: 700, type: 'process'},

    ];

    const cardElements = {};

    // Create and position cards
    cardsData.forEach(data => {
        const card = document.createElement('div');
        card.classList.add('card');
        if(data.type) card.classList.add(`card-${data.type}`);
        card.id = data.id;
        card.innerHTML = `<h3>${data.title}</h3><p>${data.content}</p>`;
        card.style.left = data.x + 'px';
        card.style.top = data.y + 'px';
        container.appendChild(card);
        cardElements[data.id] = card;

        // Make card draggable
        makeDraggable(card);
    });

    // Draw initial lines
    drawAllLines();

    function makeDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        element.onmousedown = dragMouseDown;

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
            element.style.cursor = 'grabbing';
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
            drawAllLines(); // Redraw lines as card moves
        }

        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
            element.style.cursor = 'grab';
        }
    }

    function drawLine(card1Id, card2Id) {
        const card1 = cardElements[card1Id];
        const card2 = cardElements[card2Id];

        if (!card1 || !card2) return;

        const x1 = card1.offsetLeft + card1.offsetWidth / 2;
        const y1 = card1.offsetTop + card1.offsetHeight / 2;
        const x2 = card2.offsetLeft + card2.offsetWidth / 2;
        const y2 = card2.offsetTop + card2.offsetHeight / 2;

        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', '#007bff');
        line.setAttribute('stroke-width', '2');
        svg.appendChild(line);
    }

    function drawAllLines() {
        // Clear existing lines
        while (svg.firstChild) {
            svg.removeChild(svg.firstChild);
        }
        // Redraw all lines
        cardsData.forEach(data => {
            if (data.connections) {
                data.connections.forEach(targetId => {
                    drawLine(data.id, targetId);
                });
            }
        });
    }
});