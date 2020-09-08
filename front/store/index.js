export const state = () => ({
  me: {},
  lists: [],
  list_num: 2,
})

export const mutations = {
  setMe(state, payload) {
    state.me = payload
  },
  setLists(state, payload) {
    state.lists = payload
  },
  addList(state, payload) {
    state.lists.unshift(payload)
  },
  deleteList(state, payload) {
    // state.lists.unshift(payload)
    state.lists.splice(payload, 1)
  },
  setUsers(state, payload) {
    state.lists[payload.index].users = payload.users
  },
  deleteUser(state, payload) {
    state.lists[payload.list_index].users.splice(payload.user_index, 1)
  },
  setListNum(state, payload) {
    state.list_num = payload
  },
}

export const actions = {
  setMe({ commit }, payload) {
    commit('setMe', payload)
  },
  setLists({ commit }, payload) {
    commit('setLists', payload)
  },
  addList({ commit }, payload) {
    commit('addList', payload)
  },
  deleteList({ commit }, payload) {
    commit('deleteList', payload)
  },
  setUsers({ commit }, payload) {
    commit('setUsers', payload)
  },
  deleteUser({ commit }, payload) {
    commit('deleteUser', payload)
  },
  setListNum({ commit }, payload) {
    commit('setListNum', payload)
  },
}

export const getters = {
  users: (state) => (index) => {
    return state.lists[index].users
  },
}
