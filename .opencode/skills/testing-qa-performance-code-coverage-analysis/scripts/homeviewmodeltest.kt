// Coverage for ViewModel with Android dependencies
@RunWith(RobolectricTest::class)
class HomeViewModelTest {

    @Test
    fun `given network success, when load called, then state is loaded`() = runTest {
        val dispatcher = StandardTestDispatcher(testScheduler)
        val viewModel = HomeViewModel(fakeRepository, dispatcher)

        viewModel.load()
        advanceUntilIdle()

        assertThat(viewModel.uiState.value).isInstanceOf(HomeUiState.Loaded::class.java)
    }
}