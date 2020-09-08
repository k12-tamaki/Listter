<template lang="pug">
  v-app
    v-app-bar.primary(:clipped-left="clipped" fixed app dark)
      v-toolbar-title {{title}}
      v-spacer
      v-btn(icon @click.stop="drawer = !drawer")
        v-icon mdi-menu

    v-main
      nuxt

    v-navigation-drawer(v-model="drawer" right temporary fixed dark)
      v-list
        v-list-item
          v-list-item-avatar
            v-img(:src="me.profile_image")
          v-list-item-content
            v-list-item-title {{me.name}} @{{me.screen_name}}
        v-divider
        v-list-item(@click.native="logout" link)
          v-list-item-action
            v-icon(color="white") edit
          v-list-item-title ログアウト
        v-divider
        v-list-item
          v-list-item-title
            v-text-field(
              type="number"
              v-model="edit_list_num"
              label="表示リスト数"
              :rules="[rules.required, rules.number]"
            )
          v-list-item-action
            v-btn(icon @click.stop="onClickListNum")
              v-icon(color="white") check
        v-divider
        v-list-item(@click.native="create_list_dialog = true" link)
          v-list-item-action
            v-icon(color="white") edit
          v-list-item-title リスト作成

    v-footer(:absolute="!fixed" app)
      span © {{ new Date().getFullYear() }} katsunari tamaki

    v-dialog(v-model="create_list_dialog" max-width="350")
      v-card
        v-toolbar(color="deep-purple accent-4" dark)
            v-toolbar-title 新しいリストを作成
            v-spacer
            v-btn(icon @click="create_list_dialog = false")
              v-icon cancel
        v-card-text.mt-5
          v-text-field(
            v-model="list_name"
            label="名前"
            :rules="[rules.required, rules.counter25]"
            counter
            maxlength="25"
          )
          v-text-field(
            v-model="list_description"
            label="詳細"
            :rules="[rules.counter100]"
            counter
            maxlength="100"
          )
          v-checkbox(
            v-model="is_private"
            label="非公開にする"
            color="info"
            hide-details
          )
        v-card-actions
          v-spacer
          v-btn(
            color=""
            text
            @click="create_list"
          ) 作成


</template>

<script>
import { mapState, mapActions } from 'vuex'

import firebase from '~/plugins/firebase.js'

export default {
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      miniVariant: false,
      title: 'Listter',
      create_list_dialog: false,
      list_name: '',
      list_description: '',
      is_private: true,
      edit_list_num: 0,
      rules: {
        required: (value) => !!value || 'Required',
        counter25: (value) => value.length <= 25 || 'Max 25 characters',
        counter100: (value) => value.length <= 100 || 'Max 100 characters',
        number: (value) => Number.isInteger(Number(value)) || 'Number',
      },
    }
  },
  computed: {
    ...mapState(['me', 'lists', 'list_num']),
  },
  mounted() {
    this.edit_list_num = this.list_num
  },
  methods: {
    ...mapActions(['addList', 'setListNum']),
    async create_list() {
      try {
        const response = await this.$axios.$post('/list', {
          name: this.list_name,
          description: this.list_description,
          mode: this.is_private ? 'private' : 'public',
        })
        if (response.statusCode === 200) {
          this.addList(JSON.parse(response.body))
          this.$toast.success('リスト【' + this.list_name + '】を追加しました')

          this.list_name = ''
          this.list_description = ''
          this.is_private = true

          this.create_list_dialog = false
        } else {
          console.log(response)
          this.$toast.error(response.errorMessage)
        }
      } catch (err) {
        console.log(err)
        this.$toast.error('システムエラー')
      }
    },
    onClickListNum() {
      const num = Number(this.edit_list_num)
      if (!Number.isInteger(num)) {
        this.$toast.error('整数を入力してください')
        return
      }
      if (this.lists.length < num) {
        this.$toast.error('リスト数より小さい数字を入力してください')
        return
      }
      this.setListNum(num)
      this.drawer = false
    },
    logout() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('secret')
          this.$router.push('Login')
        })
        .catch((error) => {
          this.$toast.error(`ログアウト時にエラーが発生しました (${error})`)
        })
    },
  },
}
</script>
