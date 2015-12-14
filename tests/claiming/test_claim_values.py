deploy_contracts = [
    "CallLib",
    "Scheduler",
    "AccountingLib",
    "TestCallExecution",
    "TestDataRegistry",
]


def test_claim_block_values(deploy_client, deployed_contracts,
                            deploy_future_block_call, denoms, FutureBlockCall,
                            CallLib, SchedulerLib, get_call,
                            get_execution_data):
    client_contract = deployed_contracts.TestCallExecution
    call = deploy_future_block_call(
        client_contract.setBool,
        target_block=deploy_client.get_block_number() + 1000,
        payment=denoms.ether,
    )

    target_block = call.target_block()
    base_payment = call.base_payment()

    first_claim_block = target_block - 255 - 10
    peak_claim_block = target_block - 10 - 15
    last_claim_block = target_block - 10

    assert call.get_bid_amount_for_block(first_claim_block) == 0

    for i in range(240):
        assert call.get_bid_amount_for_block(first_claim_block + i) == base_payment * i / 240

    assert call.get_bid_amount_for_block(peak_claim_block) == call.base_payment()

    for i in range(15):
        assert call.get_bid_amount_for_block(peak_claim_block + i) == call.base_payment()

    assert call.get_bid_amount_for_block(last_claim_block) == call.base_payment()