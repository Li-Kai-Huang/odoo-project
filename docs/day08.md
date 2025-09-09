# Day 08 --- 建立「隊伍管理」模組：Team / Member 資料模型

今天的進度有點像是在蓋一棟樓：\
昨天我們打好地基（ORM，資料表結構），今天終於把牆壁和窗戶裝上去了。\
簡單講：有了 Team / Member 的 Model，還要有
**搜尋、篩選、分組**的能力，這樣才算是一個「能用」的 App。\
否則所有資料都要土法煉鋼翻 SQL，就跟沒電梯的 20 樓老公寓一樣，累死人。

------------------------------------------------------------------------

## 1) 重點目標

- **Team 模型**：隊伍名稱、描述、專案關聯、成員清單。\
- **Member 模型**：姓名、角色（教練/組長/隊員）、連到 `res.users`。\
- **Search View**：讓人可以找隊伍，不用翻到眼睛脫窗。\
- **Filter & Group By**：
  - 篩選「有專案的隊伍」\
  - 依 Project 分組顯示\
- 最後做出 **UI 互動** → 就像 Google Sheet
    的篩選器一樣，管理隊伍一鍵到位。

------------------------------------------------------------------------

## 2) 程式亮點

- **分檔設計**：\
    把 `Team` 和 `Member` 拆成兩個 .py，乾淨俐落，免得 import 打架。

- **Search View** (team_views.xml 範例)：

    ``` xml
    <record id="view_team_search" model="ir.ui.view">
      <field name="name">team.management.team.search</field>
      <field name="model">team.management.team</field>
      <field name="arch" type="xml">
        <search>
          <field name="name"/>
          <field name="description"/>
          <filter string="Has Project" name="has_project" domain="[('project_id','!=',False)]"/>
          <group expand="1" string="Group By">
            <filter string="Project" context="{'group_by':'project_id'}"/>
          </group>
        </search>
      </field>
    </record>
    ```

    👉 這段就是 UI 上的 **搜尋列 + 篩選器 + 分組功能**的魔法來源。

------------------------------------------------------------------------

## 3) 實測成果

- **清單頁** → 可以直接看到所有隊伍（test、aaa、Ironman Devs）。\
- **篩選器** → 點「Has Project」，馬上過濾掉沒綁 Project 的隊伍。\
- **分組依據** → Group By Project，隊伍自動歸類。\
- **Kanban / Tree / Form** → 視圖之間能自由切換，使用體驗升級。

UI 看起來就是標準 Odoo
風格，但我們心裡知道：這其實是我們自己從零寫出來的 🛠️。

------------------------------------------------------------------------

## 4) 今日驗收清單

- [x] Team / Member 拆檔，模組結構更清晰\
- [x] Search View + Filter + Group By 上線\
- [x] 測試畫面能順利跑，沒有再報 XML error\
- [x] Kanban、List、Form 都能互動

------------------------------------------------------------------------

## 5) 明日預告（Day 09）

明天要進入更硬的東西：\
新模組「零件庫存 (Parts / Stock)」。\
這就好比一個隊伍的武器庫，隊員沒有螺絲起子和零件，就跟沒有輪子的車一樣，性能再好一樣不能動。

所以，Day 09 我們要幫 Odoo 加上「零件管理」這項超能力！⚡
