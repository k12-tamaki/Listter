<template lang="pug">
  v-btn(v-if="disp_btn" @click="loginTwitter()") Twitter連携
</template>

<script>
import firebase from '~/plugins/firebase.js'

export default {
  data() {
    return {
      disp_btn: false,
    }
  },
  computed: {},
  mounted() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        this.loginTwitter()
      } else {
        this.disp_btn = true
      }
    })
  },
  methods: {
    loginTwitter() {
      firebase
        .auth()
        .getRedirectResult()
        .then((result) => {
          this.setToken(result.credential)
        })
        .catch((error) => {
          console.log(error)
          this.$toast.error('システムエラー')
        })
    },
    setToken(credential) {
      if (credential) {
        localStorage.setItem('access_token', credential.accessToken)
        localStorage.setItem('secret', credential.secret)
        this.$router.push('List')
      } else {
        const provider = new firebase.auth.TwitterAuthProvider()
        firebase.auth().signInWithRedirect(provider)
      }
    },
  },
}
</script>
