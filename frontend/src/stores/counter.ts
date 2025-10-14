import { defineStore } from 'pinia'

interface CounterState {
  counter: number
}

export const useCounterStore = defineStore('counter', {
  state: (): CounterState => ({
    counter: 0
  }),
  getters: {
    doubleCount: (state): number => state.counter * 2
  },
  actions: {
    increment(): void {
      this.counter++
    }
  }
})
