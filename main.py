from optparse import OptionParser

from app.apriori import get_transaction_data


# get options
optparser = OptionParser()
optparser.add_option(
    '-m', '--mode',
    dest='mode',
    help='Run mode: web or commandline',
    default='web'
)
optparser.add_option(
    '-f', '--infile',
    dest='fpath',
    help='CSV filename',
    default=None
)
optparser.add_option(
    '-s', '--min_sup',
    dest='min_sup',
    help='Min support (int)',
    default=2,
    type='int'
)
(options, args) = optparser.parse_args()

# read data and prepare it to processing
if options.mode == 'commandline':
    from app.apriori import get_rules

    transaction_data = [
        {1, 2, 5},
        {2, 4},
        {2, 3},
        {1, 2, 4},
        {1, 3},
        {2, 3},
        {1, 3},
        {1, 2, 3, 5},
        {1, 2, 3}
    ]
    min_sup = options.min_sup
    if options.fpath:
        transaction_data = get_transaction_data(options.fpath)

    associated_rules = get_rules(transaction_data, min_sup)

    # Print all results
    print(f'Supported rules are: {associated_rules}')
    print(f'Total items: {len(associated_rules)}')
else:
    from app import app
    app.run(debug=True)
