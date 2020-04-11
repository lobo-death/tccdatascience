options_bovino = [
        {
            'type': "instructions",
            'text': "Você escolheu a opção bovinos, veja o que temos disponível: ",
            'ssml': """
                                <speak>
                                    <p>Você escolheu bovinos. Veja o que temos disponível.</p>
                                    <p>Maminha Ângus</p>
                                    <p>R$ 45,99</p>
                                    <p>Picanha Argentina Angus</p>
                                    <p>R$ 79,99</p>
                                    <p>Chorizo Ângus</p>
                                    <p>R$ 52,99</p>
                                    <p>Entrecôt Ângus</p>
                                    <p>R$ 59,99</p>                    
                                 </speak> """
        },
        {
            'type': "item",
            'code': "1",
            'description': 'Maminha Angus',
            'price': '45,99',
            'option': 'maminha'
        },
        {
            'type': "item",
            'code': "2",
            'description': 'Picanha Argentina Angus',
            'price': '79,99',
            'option': 'picanha'
        },
        {
            'type': "item",
            'code': "3",
            'description': 'Chorizo Angus',
            'price': '52,99',
            'option': 'chorizo'
        },
        {
            'type': "item",
            'code': "4",
            'description': 'Entrecôt Angus',
            'price': '59,99',
            'option': 'entrecot'
        },
        {
            'type': "action",
            'code': "-1",
            'description': 'Voltar',
            'price': '59,99',
            'option': 'entrecot'
        }
    ]

options_aves = [
    {
        'type': "instructions",
        'text': "Você escolheu a opção aves, veja o que temos disponível: ",
        'ssml': """
                                <speak>
                                    <p>Você escolheu aves. Veja o que temos disponível.</p>
                                    <p>Peito</p>
                                    <p>R$ 16,99</p>
                                    <p>Tulipinha</p>
                                    <p>R$ 22,99</p>
                                    <p>Coxa</p>
                                    <p>R$ 19,99</p>
                                    <p>Coração</p>
                                    <p>R$ 12,99</p>                    
                                 </speak> """
    },
    {
        'type': "item",
        'code': "5",
        'description': 'Peito',
        'price': '16,99',
        'option': 'peito'
    },
    {
        'type': "item",
        'code': "6",
        'description': 'Tulipinha',
        'price': '22,99',
        'option': 'tulipinha'
    },
    {
        'type': "item",
        'code': "7",
        'description': 'Coxa',
        'price': '19,99',
        'option': 'coxa'
    },
    {
        'type': "item",
        'code': "8",
        'description': 'Coração',
        'price': '12,99',
        'option': 'coracao'
    },
    {
        'type': "action",
        'code': "-1",
        'description': 'Voltar',
        'price': '',
        'option': 'voltar'
    }
]

options_suinos = [
    {
        'type': "instructions",
        'text': "Você escolheu a opção suínos, veja o que temos disponível: ",
        'ssml': """
                                <speak>
                                    <p>Você escolheu suínos. Veja o que temos disponível.</p>
                                    <p>Lombinho</p>
                                    <p>R$ 13,99</p>
                                    <p>Panceta</p>
                                    <p>R$ 10,99</p>
                                    <p>Linguiça Toscana</p>
                                    <p>R$ 9,99</p>                  
                                 </speak> """
    },
    {
        'type': "item",
        'code': "9",
        'description': 'Lombinho',
        'price': '13,99',
        'option': 'lombinho'
    },
    {
        'type': "item",
        'code': "10",
        'description': 'Panceta',
        'price': '10,99',
        'option': 'panceta'
    },
    {
        'type': "item",
        'code': "11",
        'description': 'Linguiça Toscana',
        'price': '9,99',
        'option': 'linguica'
    },
    {
        'type': "action",
        'code': "-1",
        'description': 'Voltar',
        'price': '',
        'option': 'voltar'
    }
]
