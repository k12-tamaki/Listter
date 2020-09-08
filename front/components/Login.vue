<template lang="pug">
</template>

<script>
import firebase from '~/plugins/firebase.js'

export default {
  data() {
    return {}
  },
  computed: {},
  mounted() {
    this.loginTwitter()
  },
  methods: {
    loginTwitter() {
      firebase
        .auth()
        .getRedirectResult()
        .then((result) => {
          if (result.credential) {
            localStorage.setItem('access_token', result.credential.accessToken)
            localStorage.setItem('secret', result.credential.secret)
            this.$router.push('List')
          } else {
            const provider = new firebase.auth.TwitterAuthProvider()
            firebase.auth().signInWithRedirect(provider)
          }
        })
        .catch((error) => {
          console.log(error)
          this.$toast.error('システムエラー')
        })
    },
  },
}
</script>
