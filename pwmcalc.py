"""
    Microchip 8bit PWM calculator.
    ------------------------------
    Use this to calculate 8bit Pic's PWM period, freuency,
    PR2 register, PWM resolution by spliting the 10bit resolution
    to the 2 lsb bits going on CCP1CON<DC1B1:DC1B0> register
    and the rest 8 msb bits on CCPR1L.
    -----------------------------------------------------------
    Microchip's instructions for PIC12F609/615/617/12HV609/615:
    11.3.7 SETUP FOR PWM OPERATION
    The following steps should be taken when configuring
    the CCP module for PWM operation:
    1. Disable the PWM pin (CCP1) output drivers by
    setting the associated TRIS bit.
    2. Set the PWM period by loading the PR2 register.
    3. Configure the CCP module for the PWM mode
    by loading the CCP1CON register with the
    appropriate values.
    4. Set the PWM duty cycle by loading the CCPR1L
    register and DC1B bits of the CCP1CON register.
    5. Configure and start Timer2:
     - Clear the TMR2IF interrupt flag bit of the PIR1
       register.
     - Set the Timer2 prescale value by loading the
       T2CKPS bits of the T2CON register.
     - Enable Timer2 by setting the TMR2ON bit of
       the T2CON register.
    6. Enable PWM output after a new PWM cycle has
    started:
    - Wait until Timer2 overflows (TMR2IF bit of the
      PIR1 register is set).
    - Enable the CCP1 pin output driver by clearing
      the associated TRIS bit.
    ########################
    # Created on 20/Feb/2022
    # Author = G.Nikolaidis
    # Version 1.00
    ########################
    Use this script on your own risk.
"""
from __future__ import print_function
import os
import math

os.system('clear')

def check_pr2(pr2val):
    """
        Check if values entered are valid
        Note: But, if a PR2 value is exceeding 8-bit value i.e.
        255 then we have to increase Timer2 pre-scale value.
    """
    while pr2val < 0 or pr2val > 255:
        print("Invalid value please enter a value between (0-255)")
        pr2val = int(raw_input("Enter PR2 (valid values 0-255):"))
    return pr2val

def check_tmr(tmr_val):
    """
        Check for TMR2 value
    """
    _dummy = True
    while _dummy:
        if int(tmr_val) == 1 or int(tmr_val) == 4 or int(tmr_val) == 16:
            _dummy = None
        else:
            print("Invalid value please enter values (1 or 4 or 16)")
            tmr_val = int(raw_input("Enter TMR (valid values 1,4,16):"))
    return tmr_val

def calc_pwm():
    """
        This function will ask from the user to enter the FOSC of the pic, the PR2 value
        and TMR to be used. It will print the TOSC, PWM period and frequency in Khz
        At PWM frequency as 78.125 kHz, your number of count for PWM period
        would be: 20,000,000/78,125 = 256 = 0x100.
    """
    print("\nFormula used to calculate PWM:")
    print("TOSC = 1/FOSC")
    print("PWM period = (PR2+1)*4*TOSC*TMR")
    print("Freq = (1/PWM period)/1000")
    print("PWM res = log(4*(PR2+1))/log(2)")
    fosc = raw_input("\nEnter FOSC freq in hz (4000000 for 4Mhz):")
    tosc = 1/float(fosc)
    _tosc = "{:.9f}".format(tosc)
    nano_sec = (float(_tosc)*1000000000)
    pr2 = int(raw_input("Enter PR2 (valid values 0-255):"))
    pr2 = check_pr2(pr2)
    tmr = int(raw_input("Enter TMR (valid values 1,4,16):"))
    tmr = check_tmr(tmr)

    pwm_p = (pr2+1)*4*tosc*tmr
    _pwmp = "{:.9f}".format(pwm_p)
    micro_sec = (float(_pwmp)*1000000)
    print("TOSC={} ns" .format(nano_sec))
    print("PWM period={} usec" .format(micro_sec))

    freq = (1/pwm_p)/1000
    print("Freq={:.4f}Khz" .format(freq))
    pwm_res = math.log(4*(pr2+1))/math.log(2)
    print("PWM Resolution in bits={:.2f}" .format(pwm_res))
    _unused = raw_input("\nHit enter to continue")

def calc_pr2_pwm_p():
    """
        Calculate PR2 value when you know pwm period
    """
    print("\nFormula used to calculate PR2:")
    print("RP2 = ((PWM period)/(4*TOSC*TMR2))-1")
    fosc = int(raw_input("\nPlease enter FOSC freq in hz (4000000 for 4Mhz): "))
    tmr2 = int(raw_input("Enter TMR2 (valid values 1,4,16): "))
    tmr2 = check_tmr(tmr2)
    pwm_per = float(raw_input("Please enter PWM period usec (100 for 100usec): "))
    pwm_pe = (pwm_per/1000000)
    tosc = 1/float(fosc)
    pr2 = int(((pwm_pe)/(4*tosc*tmr2))-1)
    if pr2 > 255:
        print("PR2 value is higher that 255, please consider increase \
             \nTimer2 pre-scale value and try again!")
    print("PR2={}(decimal)" .format(pr2))
    print("PR2={}(hex)" .format(hex(pr2).upper()))
    _unused = raw_input("\nHit enter to continue")

def calc_pr2():
    """
        This function will ask from the user the FOSC freq the RP2
        and the desired PWM output freq, to calculate the PWM resolution.
    """
    print("\nFormula used to calculate PR2:")
    print("RP2 = ((FOSC)/(4*TMR2*PWM))-1")
    fosc = int(raw_input("\nPlease enter FOSC freq in hz (4000000 for 4Mhz): "))
    tmr2 = int(raw_input("Enter TMR2 (valid values 1,4,16): "))
    tmr2 = check_tmr(tmr2)
    pwm = int(raw_input("Enter PWM freq in hz (1000 for 1Khz): "))
    pr2 = ((fosc)/(4*tmr2*pwm))-1
    if pr2 > 255:
        print("PR2 value is higher that 255, please consider increase \
             \nTimer2 pre-scale value and try again!")
    print("PR2={}(decimal)" .format(pr2))
    print("PR2={}(hex)" .format(hex(pr2).upper()))
    _unused = raw_input("\nHit enter to continue")

def calc_pwm_res():
    """
        This function will ask from the user to enter the PR2 value
        and Duty Cycle to be used i.e 50 for 50% Duty Cycle. It will print the
        resolution of PWM. Resolution of a PWM is the number of different steps
        you can have from zero power to full power. That is a 10 bit resolution
        means that you can have 1024 steps from zero to full power. For 6 bit
        you can have only 63 steps.
    """
    print("\nFormula used to calculate PWM resolution:")
    print("log(4*(PR2+1))/log(2)")
    fosc = int(raw_input("\nEnter FOSC freq in hz (4000000 for 4Mhz):"))
    pr2 = int(raw_input("Enter PR2 (valid values 0-255):"))
    pr2 = check_pr2(pr2)
    fpwm = int(raw_input("Enter freq of PWM in hz (1000 for 1Khz):"))
    #FPWM is the desired PWM output frequency

    pwm_res = math.log(4*(pr2+1))/math.log(2)
    print("PWM Resolution in bits={:.2f}" .format(pwm_res))

    res2 = math.log(fosc/fpwm)/math.log(2)
    print("PWM Resolution using different formula")
    print("log(FOSC/PWM_freq)/log(2)={:.2f}" .format(res2))
    _unused = raw_input("\nHit enter to continue")

def calc_prl1_con():
    """
        This script will ask from the user to enter the PR2 value
        and Duty Cycle to be used. It will print the CCPR1L: CCP1CON<5:4>
        Note:
        CCP1CON = 0x0C;	/* Set PWM mode and no decimal for PWM */
    """
    print("\nFormula used to calculate CCPRL1_CCP1CON:")
    print("CCPRL1_CCP1CON = (PR2+1)*(DC/100.0)")
    pr2 = int(raw_input("\nEnter PR2 (valid values 0-255):"))
    pr2 = check_pr2(pr2)
    duty_cycle = int(raw_input("Enter Duty Cycle (ie. 50 for 50%):"))

    while duty_cycle < 0 or duty_cycle > 100:
        print("Invalid value please enter a value between (0-100)")
        duty_cycle = int(raw_input("Enter Duty Cycle (ie. 50 for 50%):"))

    ccprl1_ccp1con = round(4*(pr2+1)*(duty_cycle/100.0))
    ccpcon = int("{:.0f}" .format(ccprl1_ccp1con))
    if ccpcon > 1024:
        pront("CCPRL1_CCP1CON is grader than 10bit (1024) 8bit MCU \
             \nsupport up to 10bit PWM resolution, try again!!")
    result = ccpcon & 1
    if result == 1:
        bit0 = 1
    else:
        bit0 = 0
    result = ccpcon & 2
    if result == 2 and bit0 == 1:
        bit0 = 3
    if result == 2 and bit0 == 0:
        bit0 = 2
    if result == 0 and bit0 == 0:
        bit0 = 0
    if result == 0 and bit0 == 1:
        bit0 = 1
    ccprl1 = ccpcon >> 2
    print("CCPRL1_CCP1CON={}(decimal)" .format(ccpcon))
    bin_ccp = format(ccpcon, '010b')
    print("CCPRL1_CCP1CON={}" .format(bin_ccp))
    ccp1con = format(bit0, '02b')
    print("CCP1CON<DC1B1:DC1B0>={}" .format(ccp1con))
    ccprl = format(ccprl1, '08b')
    print("CCPR1L={}" .format(ccprl))
    _unused = raw_input("\nHit enter to continue")


# main function
ANS = True
while ANS:
    print("******** Welcome to 8bit Pic PWM calculations ********")
    print("******************************************************")
    CHOICE = raw_input("1: PWM period and freq\n2: PR2\n3: PR2 when PWM period known \
                       \n4: PWM resolution \
                       \n5: CCPR1L CCP1CON regs \
                       \n6: Clear screen\n7: Exit\nPlease enter your CHOICE: ")

    if CHOICE == '1':
        calc_pwm()
    elif CHOICE == '2':
        calc_pr2()
    elif CHOICE == '3':
        calc_pr2_pwm_p()
    elif CHOICE == '4':
        calc_pwm_res()
    elif CHOICE == '5':
        calc_prl1_con()
    elif CHOICE == '6':
        os.system('clear')
    elif CHOICE == '7':
        print("\nSagionara!")
        ANS = None
    else:
        print("You must only select either 1,2,3,4 or 5")
        print("Please try again")
#EOF
