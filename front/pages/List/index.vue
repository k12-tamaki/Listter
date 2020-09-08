<template lang="pug">
  v-container(fluid).list
    v-row(no-gutters)
      v-col(cols="4")
        v-card.mx-auto(v-if="follow" max-width="500")
          v-toolbar(color="deep-purple accent-4" dark)
            v-badge(color="info")
              template(v-slot:badge) {{follow_length}}
              v-toolbar-title {{follow.name}}
            v-spacer
            v-btn(icon @click="refresh_follow")
              v-icon refresh
          v-list
            draggable(
              v-model="follow.users"
              v-bind="follow_options"
              tag="ul"
              data-column-id=""
              @end="get_follow_to_list"
            )
              v-list-item(
                v-for="user, user_index in follow.users"
                :key="user.is_str"
                :data-id="user.is_str"
                @click=""
              )
                v-list-item-avatar
                  v-img(:src="user.profile_image")
                v-list-item-content
                  v-list-item-title
                    div {{user.name}} @{{user.screen_name}}
                    template(v-for="list in user.lists")
                      v-chip(v-if="list.is_conf" x-small color="info") {{list.name}}
                      v-chip(v-if="!list.is_conf" x-small color="warning") {{list.name}}

      v-col(cols="8")
        v-row(no-gutters).lists
          v-col.ml-3.mb-1(cols="5" v-for="n of list_num" :key="n")
            Detail2(
              v-if="lists.length != 0"
              :card-index="n - 1"
              @save="onSave"
              @delete="onDeleteList"
              @dragg="get_follow_to_list"
              :ref="'card' + String(n - 1)"
            )
          //- v-col.ml-3.mb-3(cols="5" v-for="list, list_index in lists" :key="list.id_str")
          //-   Detail(
          //-     :list="list"
          //-     :list-index="list_index"
          //-     @save="onSave"
          //-     @delete="onDeleteList"
          //-     @dragg="get_follow_to_list"
          //-   )

    v-dialog(v-model="delete_conf_dialog" max-width="350")
      v-card
        v-card-title 削除確認
        v-card-text 【{{delete_list.name}}】を削除します。よろしいですか？
        v-card-actions
          v-spacer
          v-btn(
            color="green"
            text
            @click="onDeleteListConf"
          ) Yes
          v-btn(
            color=""
            text
            @click="delete_conf_dialog = false"
          ) No

</template>

<script>
import { mapState, mapActions } from 'vuex'
import draggable from 'vuedraggable'

import Detail from '@/components/detail'
import Detail2 from '@/components/detail2'

export default {
  components: { draggable, Detail, Detail2 },
  data: () => ({
    follow_options: {
      group: {
        name: 'user',
        pull: 'clone',
        put: false,
      },
      animation: 100,
      sort: false,
    },
    follow: null,
    delete_conf_dialog: false,
    delete_list: {},
    delete_list_index: null,
    delete_card_index: null,
  }),
  computed: {
    ...mapState(['lists', 'list_num']),
    follow_length() {
      return this.follow.users ? this.follow.users.length : null
    },
  },
  created() {
    this.init()
  },
  methods: {
    ...mapActions(['setMe', 'setLists', 'deleteList']),
    async init() {
      const status = await this.get_me()
      if (!status) {
        this.$router.push('Login')
        return
      }

      await Promise.all([this.get_follow(), this.get_lists()])
      // await Promise.all([this.test_follow(), this.test_lists()])
      this.get_follow_to_list()
    },
    async refresh_follow() {
      await this.get_follow()
      this.get_follow_to_list()
    },
    async get_me() {
      // ユーザー情報を取得とキーが正しいかチェック
      this.setMe({})
      if (
        !localStorage.getItem('access_token') ||
        !localStorage.getItem('secret')
      ) {
        console.log('non token')
        return false
      }
      try {
        const response = await this.$axios.$get('/me')
        if (response.statusCode === 200) {
          this.setMe(JSON.parse(response.body))
          return true
        } else {
          console.log(response)
          this.$toast.error(response.errorMessage)
          return false
        }
      } catch (err) {
        console.log(err)
        this.$toast.error('システムエラー')
        return false
      }
    },
    async get_follow() {
      // followを取得
      this.follow = null
      try {
        const response = await this.$axios.$get('/follow')
        if (response.statusCode === 200) {
          this.follow = {
            id_str: '',
            name: 'フォロー',
            users: JSON.parse(response.body),
          }
        } else {
          console.log(response)
          this.$toast.error(response.errorMessage)
        }
      } catch (err) {
        console.log(err)
        this.$toast.error('システムエラー')
      }
    },
    test_follow() {
      // followを取得
      this.follow = {
        id_str: '',
        name: 'フォロー',
        users: [
          {
            id_str: '111',
            name: 'test1_user',
            screen_name: 'テスト1ユーザー',
            profile_image: '',
          },
          {
            id_str: '222',
            name: 'test2_user',
            screen_name: 'テスト2ユーザー',
            profile_image: '',
          },
        ],
      }
    },
    async get_lists() {
      this.setLists([])

      try {
        // リストと、そのユーザーを取得
        const response = await this.$axios.$get('/list')
        if (response.statusCode === 200) {
          this.setLists(JSON.parse(response.body))
        } else {
          console.log(response)
          this.$toast.error(response.errorMessage)
        }
      } catch (err) {
        console.log(err)
        this.$toast.error('システムエラー')
      }
    },
    test_lists() {
      this.setLists([])

      const lists = [
        {
          id_str: '11',
          name: 'テストリスト',
          users: [
            {
              id_str: '',
              name: 'test_user',
              screen_name: 'テストユーザー',
              profile_image: '',
            },
          ],
        },
      ]
      this.setLists(lists)
    },
    get_follow_to_list() {
      this.follow.users.forEach((user) => {
        user.lists = []
        this.lists.forEach((list) => {
          const arrayIdStr = list.users.map((user) => user.id_str)

          if (arrayIdStr.includes(user.id_str)) {
            user.lists.push({
              name: list.name,
              is_conf: true,
            })
          }
        })
      })
    },
    async onSave(list) {
      const usersIdArr = list.users.map((obj) => obj.id_str)

      try {
        const response = await this.$axios.$post('/list/members', {
          list_id: list.id_str,
          user_ids: usersIdArr,
        })
        if (response.statusCode === 200) {
          this.$toast.success('リスト【' + list.name + '】を登録しました')
        } else {
          console.log(response)
          this.$toast.error(response.errorMessage)
        }
      } catch (err) {
        console.log(err)
        this.$toast.error('システムエラー')
      }
    },
    onDeleteList(list, listIndex, cardIndex) {
      this.delete_list = list
      this.delete_list_index = listIndex
      this.delete_card_index = cardIndex
      this.delete_conf_dialog = true
    },
    async onDeleteListConf() {
      try {
        const response = await this.$axios.$delete('/list', {
          data: {
            id: this.delete_list.id_str,
          },
        })
        if (response.statusCode === 200) {
          this.$toast.success(
            'リスト【' + this.delete_list.name + '】を削除しました'
          )
          this.deleteList(this.delete_list_index)
          this.$refs['card' + this.delete_card_index][0].deleteList()
          this.get_follow_to_list()
          this.delete_conf_dialog = false
        } else {
          console.log(response)
          this.$toast.error(response.errorMessage)
        }
      } catch (err) {
        console.log(err)
        this.$toast.error('システムエラー')
      }
    },
  },
}
</script>

<style scoped>
.lists {
  height: calc(100vh - 130px);
  overflow-y: scroll;
}
.v-list {
  height: calc(100vh - 200px);
  overflow-y: scroll;
}
</style>
