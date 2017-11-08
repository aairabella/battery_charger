# All the imports....
import argparse
from power import Hantek_PPS2116A
from timeit import default_timer



# Main

# Init Power Suppy

# Parse Arguments

# Main Loop. It stops when the battery "charged" condition is reached. 

def setup_power_sypply(power_supply, voltage, current, turn):
    power_supply.set_voltage(voltage=voltage)
    power_supply.set_current(current=current)

    if turn == 'on':
        power_supply.set_on()
    else:
        power_supply.set_off()

def parse_commandline():
    parser = argparse.ArgumentParser(description='Battery Charger using a Hantek Power Sypply')
  
    parser.add_argument('--bulk-current',       dest='bulk_current',       action='store', default=0,  help='Set Bulk status current')
    parser.add_argument('--bulk-voltage',       dest='bulk_voltage',       action='store', default=0,  help='Set Bulk status voltage')
    parser.add_argument('--absorption-current', dest='absorption_current', action='store', default=0,  help='Set Absorption status current')
    parser.add_argument('--absorption-voltage', dest='absorption_voltage', action='store', default=0,  help='Set Absorption status voltage')
    parser.add_argument('--floating-current',   dest='floating_current',   action='store', default=0,  help='Set Floating status current')
    parser.add_argument('--floating-voltage',   dest='floating_voltage',   action='store', default=0,  help='Set Floating status voltage')
    parser.add_argument('--floating-time',      dest='floating_time',      action='store', default=10, help='Set Floating Time. Default 10 minutes')
    
    return parser.parse_args()

if __name__ == '__main__':

    # Define State Machine states. 
    status_list = ['Idle', 'Bulk', 'Absorption', 'Floating', 'Finish']
    status = 'Idle'

    # Leo argumentos del script
    args                = parse_commandline()
    
    bulk_current        = float( args.bulk_current       )  
    bulk_voltage        = float( args.bulk_voltage       )
    absorption_current  = float( args.absorption_current )
    absorption_voltage  = float( args.absorption_voltage )
    floating_current    = float( args.floating_current   )
    floating_voltage    = float( args.floating_voltage   )
    floating_time       = float( args.floating_time      )
    
    print(' ------------------------------------------------')
    print(' ------------------------------------------------')
    print('| Status \t| Voltage \t| Current \t |')
    print('| Bulk   \t| %2.2f   \t| %1.3f   \t |' % (bulk_voltage, bulk_current))
    print('| Absorption\t| %2.2f   \t| %1.3f   \t |' % (absorption_voltage, absorption_current))
    print('| Floating   \t| %2.2f   \t| %1.3f   \t |' % (floating_voltage, floating_current))
    print(' ------------------------------------------------')
    print('| Floating Time: %2.2f \t\t\t\t |' % floating_time)
    print(' ------------------------------------------------')

    ps = Hantek_PPS2116A() 

    # Start Idle but configures everithung to go Bulk
    status = 'Bulk'
    setup_power_sypply(power_supply=ps, voltage=bulk_voltage, current=bulk_current, turn='on')
    start = default_timer()

    while(status != 'Finish'):
        if status == 'Bulk':
            measured_voltage = ps.read_measured_voltage()
            if measured_voltage == absorption_voltage:
                status = 'Absorption'
                setup_power_sypply(power_supply=ps, voltage=absorption_voltage, current=absorption_current, turn='on')

        elif status == 'Absorption':
            measured_current = ps.read_measured_current()
            if measured_current == absorption_current:
                status = 'Floating'
                setup_power_sypply(power_supply=ps, voltage=floating_voltage, current=floating_current, turn='on')

        elif status == 'Floating':
            measured_current = ps.read_measured_current()
            if (default_timer() - start)*60 > floating_time:
                status = 'Finish'
                setup_power_sypply(power_supply=ps, voltage=0, current=0, turn='off')

        else:
            print('I got lost in the states... please, review the code! ;-)')
            quit()

        time.sleep(1)

    print('Charge complete...')
    quit()