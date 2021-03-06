from eth_account import Account


def to_address(priv_key):
    prefix = '' if priv_key.startswith('0x') else '0x'
    return Account.privateKeyToAccount(prefix + priv_key).address


class ContractWrapper:
    def __init__(self, w3, gas_price, user_pk, **kwargs):
        """
        Методы автоматически определяются как call или buildTransaction
        > методы определенные как call возвращают результат функции
        > методы определенные как bT возвращают рецепт отправленной транзакции

        Args:
            w3 (Web3): экземпляр web33 для общения с блокчеином.
            **kwargs (type): парамтры как для eth.contract().
        """
        user_acc = to_address(user_pk)
        contract = w3.eth.contract(**kwargs)

        # setup events
        self.events = contract.events

        # setup constructor
        def construct(*args, **kwargs):
            tx = contract.constructor(*args, **kwargs).buildTransaction({
                'gasPrice': gas_price,
                'nonce':    w3.eth.getTransactionCount(user_acc)
            })

            signed = w3.eth.account.signTransaction(tx, private_key=user_pk)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            return tx_receipt

        setattr(self, 'constructor', construct)

        # setup contract methods
        for elem in kwargs['abi']:
            if 'name' in elem:
                try:
                    # choose call or buildTransaction
                    if elem['stateMutability'] in ['view', 'pure']:
                        def funct(name):
                            def func(*args, **kwargs):
                                return getattr(contract.functions, name)(*args, **kwargs).call()

                            return func
                    else:
                        def funct(name):
                            def func(*args, **kwargs):
                                value = 0 if 'value' not in kwargs.keys() else kwargs.pop('value')

                                tx = {
                                    'from':     user_acc,
                                    'to':       contract.address,
                                    'value':    value,
                                    'gasPrice': gas_price,
                                    'nonce':    w3.eth.getTransactionCount(user_acc),
                                    'data':     contract.encodeABI(fn_name=name, args=args, kwargs=kwargs)
                                }

                                tx['gas'] = w3.eth.estimateGas(tx)
                                tx['gas'] *= (1 if tx['gas'] * tx['gasPrice'] >= w3.eth.get_balance(user_acc) else 2)

                                signed = w3.eth.account.signTransaction(tx, private_key=user_pk)
                                tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                                tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

                                return tx_receipt

                            return func
                    setattr(self, elem['name'], funct(elem['name']))
                except KeyError:
                    pass
