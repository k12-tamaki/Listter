<template lang="pug">
  v-card.mx-auto(max-width="500")
    v-toolbar(color="deep-purple accent-2" dark)
      v-badge(color="info")
        template(v-slot:badge) {{list_length}}
        v-toolbar-title
          v-autocomplete(
            v-model="list"
            :items="lists"
            item-text="name"
            item-value="id_str"
            hide-details
            return-object
          )
      v-spacer
      v-btn(icon @click="onSave(list)")
        v-icon save
      v-btn(icon @click="onDeleteList(list, listIndex)")
        v-icon delete
    v-list
      draggable(
        v-model="users"
        v-bind="options"
        tag="ul"
        :data-column-id="list.id_str"
        @end="onEnd"
      )
        v-list-item(
          v-for="user, user_index in users"
          :key="user.is_str"
          :data-id="user.is_str"
          @click=""
        )
          v-list-item-avatar
            v-img(:src="user.profile_image")
          v-list-item-content
            v-list-item-title {{user.name}} @{{user.screen_name}}
          v-list-item-action
            v-btn(icon @click="onDelete(user_index)")
              v-icon(color="grey") highlight_off

</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    cardIndex: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      list: null,
      options: {
        group: 'user',
        animation: 100,
      },
    }
  },
  computed: {
    ...mapState(['lists']),
    listIndex() {
      return this.lists.findIndex((list) => {
        return list.id_str === this.list.id_str
      })
    },
    users: {
      get() {
        return this.list.users
      },
      set(val) {
        const uniqCheck = new Set(val.map((e) => JSON.stringify(e)))
        const unipArray = Array.from(uniqCheck).map((e) => JSON.parse(e))
        const payload = {
          index: this.listIndex,
          users: unipArray,
        }
        this.$store.commit('setUsers', payload)
      },
    },
    list_length() {
      return this.list.users ? this.list.users.length : null
    },
  },
  created() {
    this.list = this.lists[this.cardIndex]
  },
  methods: {
    onEnd(event) {
      this.$emit('dragg')
    },
    onDelete(userIndex) {
      const payload = {
        list_index: this.listIndex,
        user_index: userIndex,
      }
      this.$store.commit('deleteUser', payload)
      this.$emit('dragg')
    },
    onSave(list) {
      this.$emit('save', list)
    },
    onDeleteList(list, listIndex) {
      this.$emit('delete', list, listIndex, this.cardIndex)
    },
    deleteList() {
      this.list = this.lists[0]
    },
  },
}
</script>

<style scoped>
.v-list {
  height: calc(100vh - 200px);
  overflow-y: scroll;
}
</style>
