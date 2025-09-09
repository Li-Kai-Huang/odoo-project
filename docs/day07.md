# Day 07 — Odoo View 與 XML / QWeb 基礎

昨天我們在後端玩得很開心，把 ORM 抓來當小弟，隨便下個 `create()`、`search()`，資料庫就乖乖生東西。  
但用戶不可能天天在 Odoo Shell 裡敲指令吧？  
今天就是要把這些資料**拉上檯面，穿上漂亮的衣服**，靠的就是 **View + XML + QWeb**。

---

## 1) View：畫面的四大門派

Odoo 的 View 就像 UI 的「武功祕笈」，常見的招式有四種：

- **Tree View（清單大法）**  
  適合快速瀏覽，一次看多筆。  
  ```xml
  <tree>
    <field name="name"/>
    <field name="role"/>
  </tree>
  ```

- **Form View（單筆心法）**  
  單筆資料的細節編輯，必備。  
  ```xml
  <form>
    <sheet>
      <group>
        <field name="name"/>
        <field name="description"/>
      </group>
    </sheet>
  </form>
  ```

- **Kanban View（看板神功）**  
  資料變卡片，可以拖拉，管理專案超方便。  
  ```xml
  <kanban default_group_by="project_id">
    <templates>
      <t t-name="kanban-box">
        <div class="oe_kanban_global_click">
          <strong><field name="name"/></strong>
          <div><field name="description"/></div>
        </div>
      </t>
    </templates>
  </kanban>
  ```

- **Search View（搜尋祕術）**  
  幫你定義搜尋欄與篩選器，快速找到目標。  
  ```xml
  <search>
    <field name="name"/>
    <filter string="Leader" name="leader" domain="[('role','=','leader')]"/>
  </search>
  ```

---

## 2) XML：Odoo 的 UI 藍圖

XML 在 Odoo 世界裡就像建築藍圖。  
你在 XML 裡說「這裡要一個 `<field>`」，Odoo 就自動幫你跟 ORM 接好線，畫面馬上長出欄位。  

優點有三：  
1. 結構化，讀起來一清二楚  
2. 可繼承，用 `<xpath>` 輕鬆插內容  
3. 跟 ORM 綁定超緊密，欄位不必手刻  

---

## 3) QWeb：模板忍術

QWeb 就是 Odoo 的模板引擎，負責「最後一哩路」的渲染。  
不管是 Kanban 卡片還是 PDF 報表，都要靠它。

常用招式：  
- `t-esc` → 輸出文字，幫你自動 escape  
- `t-if` → 條件判斷，像 if-else  
- `t-foreach` → 迴圈神器  

範例（Kanban 卡片）：  
```xml
<t t-name="kanban-box">
  <div>
    <t t-esc="record.name.value"/>
    <t t-if="record.role.raw_value == 'leader'">
      <span class="badge">隊長</span>
    </t>
  </div>
</t>
```

結果：  
- 顯示成員名字  
- 如果是 Leader，就帥氣加上「隊長」徽章 🎖️  

---

## 4) 小試身手：QWeb 報表

假設我們想印出所有 Team 與成員名單，可以這樣寫：

```xml
<template id="report_team_list">
  <t t-call="web.html_container">
    <t t-foreach="docs" t-as="team">
      <h2><t t-esc="team.name"/></h2>
      <p><t t-esc="team.description"/></p>
      <ul>
        <t t-foreach="team.member_ids" t-as="member">
          <li><t t-esc="member.name"/> (<t t-esc="member.role"/>)</li>
        </t>
      </ul>
    </t>
  </t>
</template>
```

一旦綁定到報表 Action，就能直接下載 PDF，  
老闆看到整齊的名單，絕對比看到 `SELECT * FROM ...` 還感動 🤣。

---

## 5) 今日驗收清單

- [x] 知道 Odoo 的四大 View（Tree / Form / Kanban / Search）  
- [x] 瞭解 XML 在 Odoo 裡就是畫面藍圖  
- [x] 學會 QWeb 三大指令（t-esc / t-if / t-foreach）  
- [x] 做出一個 Kanban 卡片模板  
- [x] 嘗試用 QWeb 生出 Team + Member 名單報表  

---

## 6) 明日預告（Day 08）

明天要進入實戰，把 **OCA 模組**請進場，看看社群高手是怎麼幫我們加速專案開發的。  
資料有了、畫面也有了，接下來就是「武器升級」的時候了 ⚔️。