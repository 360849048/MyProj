<template>
  <div id="hardware-title">
    <!-- 一级菜单选择 -->
    <ul class="nav nav-tabs first-class-menu">
      <li class="nav-item" v-for="idx in TITLES.length" @click="clickOn1stClassMenu(idx)">
        <a href=""
           onclick="return false"
           class="nav-link"
           :class="{'active': curTitleIdx===idx}">
          {{TITLES[idx - 1]}}
        </a>
      </li>
    </ul>

    <!-- 二级菜单 -->
    <section>
      <!-- 主底板IO -->
      <div class="btn-group" role="group" v-if="curTitleIdx===1">
        <button type="button" class="btn btn-secondary btn-70px"
                v-for="idx in IO_TYPES.length"
                @click="clickOn2ndClassMenu(idx)"
                :class="{'active': curSlotIdx === idx}">
          {{IO_TYPES[idx - 1]}}
        </button>
      </div>

      <!-- 主底板扩展槽 -->
      <div class="btn-group btn-group-toggle" data-toggle="buttons" v-if="curTitleIdx===2">
        <div class="btn-group" v-for="slotIdx in mainBoardSlotNum">
          <button type="button" class="btn btn-secondary btn-sm btn-100px"
                  :class="{'active': curSlotIdx===slotIdx}"
                  @click="clickOn2ndClassMenu(slotIdx)">
            {{mainBoardSlots[slotIdx - 1] | toCorrectName}}
          </button>
          <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <span class="sr-only">Toggle Dropdown</span>
          </button>
          <div class="dropdown-menu">
            <a class="dropdown-item" href="##"
               v-for="(module, moduleIdx) in DIAS_MODULES"
               @click="clickOnSelectDiasModuleBtn(slotIdx, moduleIdx)">
              {{module | toCorrectName}}
            </a>
          </div>
        </div>
      </div>

      <!-- 扩展底板一扩展槽 -->
      <div class="btn-group btn-group-toggle" data-toggle="buttons" v-if="curTitleIdx===3">
        <div class="btn-group" v-for="slotIdx in extendBoard1Slots.length">
          <button type="button" class="btn btn-secondary btn-sm btn-100px"
                  :class="{'active': curSlotIdx===slotIdx}"
                  @click="clickOn2ndClassMenu(slotIdx)">
            {{extendBoard1Slots[slotIdx - 1] | toCorrectName}}
          </button>
          <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <span class="sr-only">Toggle Dropdown</span>
          </button>
          <div class="dropdown-menu" v-if="slotIdx === 1">
            <a class="dropdown-item" href="##"
               v-for="(module, moduleIdx) in CONN_MODULES"
               @click="clickOnSelectConnModuleBtn(slotIdx, moduleIdx)">
              {{module | toCorrectName}}
            </a>
          </div>
          <div class="dropdown-menu" v-else="slotIdx > 1">
            <a class="dropdown-item" href="##"
               v-for="(module, moduleIdx) in DIAS_MODULES"
               @click="clickOnSelectDiasModuleBtn(slotIdx, moduleIdx)">
              {{module | toCorrectName}}
            </a>
          </div>
        </div>
      </div>

      <!-- 扩展底板二扩展槽 -->
      <div class="btn-group btn-group-toggle" data-toggle="buttons" v-if="curTitleIdx===4">
        <div class="btn-group" v-for="slotIdx in extendBoard2Slots.length">
          <button type="button" class="btn btn-secondary btn-sm btn-100px"
                  :class="{'active': curSlotIdx===slotIdx}"
                  @click="clickOn2ndClassMenu(slotIdx)">
            {{extendBoard2Slots[slotIdx - 1] | toCorrectName}}
          </button>
          <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <span class="sr-only">Toggle Dropdown</span>
          </button>
          <div class="dropdown-menu" v-if="slotIdx===1">
            <a class="dropdown-item" href="##"
               v-for="(module, moduleIdx) in CONN_MODULES"
               @click="clickOnSelectConnModuleBtn(slotIdx, moduleIdx)">
              {{module | toCorrectName}}
            </a>
          </div>
          <div class="dropdown-menu" v-else="slotIdx > 1">
            <a class="dropdown-item" href="##"
               v-for="(module, moduleIdx) in DIAS_MODULES"
               @click="clickOnSelectDiasModuleBtn(slotIdx, moduleIdx)">
              {{module | toCorrectName}}
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    name: "hardware-title",
    props: {
      type: String,
      mainBoardSlots: Array,
      extendBoard1Slots: Array,
      extendBoard2Slots: Array,
    },
    computed: {
      mainBoardSlotNum () {
        if (this.type.toUpperCase() === 'VE2') {
          return 1;
        }
        return 4;
      }
    },
    data () {
      return {
        curTitleIdx: 1,
        curSlotIdx: 1,
        TITLES: ['主底板IO', '主底板插槽', '扩展底板一', '扩展底板二'],
        IO_TYPES: ['DI', 'DO', 'AI', 'AO', 'TI', 'TO'],
        connModules: ['', 'CIV512', 'CIV521'],
        DIAS_MODULES: ['', 'CIO021', 'CDM163', 'CTO163', 'CDI163', 'CAI888', 'CIO011'],
        CONN_MODULES: ['', 'CIV512', 'CIV521'],
      }
    },
    methods: {
      _emit (newSlotsConfig) {
        this.$emit('moduleselectupdate', {
          curTitleIdx: this.curTitleIdx,
          curSlotIdx: this.curSlotIdx,
          slots: newSlotsConfig
        })
      },
      clickOn1stClassMenu (curTitleIdx) {
        this.curTitleIdx = curTitleIdx;
        this.curSlotIdx = 1;
        let allBoardsSlots = [this.mainBoardSlots, this.extendBoard1Slots, this.extendBoard2Slots];
        this._emit(this.curTitleIdx === 1 ? [] : allBoardsSlots[this.curTitleIdx - 2]);
      },
      clickOn2ndClassMenu (curSlotIdx) {
        this.curSlotIdx = curSlotIdx;
        let allBoardsSlots = [this.mainBoardSlots, this.extendBoard1Slots, this.extendBoard2Slots];
        this._emit(this.curTitleIdx === 1 ? [] : allBoardsSlots[this.curTitleIdx - 2]);
      },
      clickOnSelectDiasModuleBtn (slotIdx, moduleIdx) {
        let curBoard = undefined;
        switch (this.curTitleIdx) {
          case 2:
            curBoard = JSON.parse(JSON.stringify(this.mainBoardSlots));
            break;
          case 3:
            curBoard = JSON.parse(JSON.stringify(this.extendBoard1Slots));
            break;
          case 4:
            curBoard = JSON.parse(JSON.stringify(this.extendBoard2Slots));
            break;
        }
        if (curBoard === undefined) {
          alert('Fatal，clickOnSelectDiasModuleBtn');
          return;
        }
        if (this.curTitleIdx > 2) {
          // 当前在扩展底板时，需要首先配置连接模块
          if (curBoard[0] === '') {
            this.$notify.error({
              title: '错误',
              message: '请先配置连接模块'
            });
            return;
          }
        }
        curBoard[slotIdx - 1] = this.DIAS_MODULES[moduleIdx];
        this._emit(curBoard);
      },
      clickOnSelectConnModuleBtn (slotIdx, moduleIdx) {
        let curBoard = undefined;
        switch (this.curTitleIdx) {
          case 3:
            curBoard = JSON.parse(JSON.stringify(this.extendBoard1Slots));
            break;
          case 4:
            curBoard = JSON.parse(JSON.stringify(this.extendBoard2Slots));
            break;
        }
        if (curBoard === undefined) {
          alert('Fatal, clickOnSelectConnModuleBtn');
          return;
        }
        // 当连接模块取消后，清空后面的模块配置
        if (moduleIdx === 0) {
          curBoard[1] = this.DIAS_MODULES[0];
          curBoard[2] = this.DIAS_MODULES[0];
          curBoard[3] = this.DIAS_MODULES[0];
        }
        curBoard[slotIdx - 1] = this.CONN_MODULES[moduleIdx];
        this._emit(curBoard);
      }
    },
    filters: {
      toCorrectName (name) {
        if (name === '') {
          return '未使用';
        } else {
          return name;
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  .first-class-menu {
    margin: 1rem 0 .5rem;
  }
  .btn-100px{
    width: 100px !important;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
  }
  .btn-70px{
    width: 70px !important;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
  }
</style>
