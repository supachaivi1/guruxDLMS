#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import os
import pdb
import sys
import traceback
from gurux_serial import GXSerial
from gurux_net import GXNet
from gurux_dlms.enums import ObjectType
from gurux_dlms.objects.GXDLMSObjectCollection import GXDLMSObjectCollection
from GXSettings import GXSettings
from GXDLMSReader import GXDLMSReader
from gurux_dlms.GXDLMSClient import GXDLMSClient
from gurux_common.GXCommon import GXCommon
from gurux_dlms.enums.DataType import DataType
import locale
from gurux_dlms.GXDateTime import GXDateTime
from gurux_dlms.internal._GXCommon import _GXCommon
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError, GXDLMSTranslator
from gurux_dlms import GXByteBuffer, GXDLMSTranslatorMessage, GXReplyData
from gurux_dlms.enums import RequestTypes, Security, InterfaceType
from gurux_dlms.secure.GXDLMSSecureClient import GXDLMSSecureClient
import sqlite3
import base64
import pandas as pd
import datetime

try:
    import pkg_resources
    # pylint: disable=broad-except
except Exception:
    # It's OK if this fails.
    print("pkg_resources not found")

list_data = list()

# pylint: disable=too-few-public-methods,broad-except
class sampleclient():
    @classmethod
    def main(cls, args):
        try:
            print("gurux_dlms version: " + pkg_resources.get_distribution("gurux_dlms").version)
            print("gurux_net version: " + pkg_resources.get_distribution("gurux_net").version)
            print("gurux_serial version: " + pkg_resources.get_distribution("gurux_serial").version)
        except Exception:
            # It's OK if this fails.
            print("pkg_resources not found")

        # args: the command line arguments
        reader = None
        settings = GXSettings()
        try:
            # //////////////////////////////////////
            #  Handle command line parameters.
            ret = settings.getParameters(args)
            if ret != 0:
                return
            # //////////////////////////////////////
            #  Initialize connection settings.
            if not isinstance(settings.media, (GXSerial, GXNet)):
                raise Exception("Unknown media type.")
            # //////////////////////////////////////
            reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
            settings.media.open()
            if settings.readObjects:
                read = False
                reader.initializeConnection()
                if settings.outputFile and os.path.exists(settings.outputFile):
                    try:
                        c = GXDLMSObjectCollection.load(settings.outputFile)
                        settings.client.objects.extend(c)
                        if settings.client.objects:
                            read = True
                    except Exception:
                        read = False
                if not read:
                    reader.getAssociationView()
                data_list = list()
                for k, v in settings.readObjects:
                    obj = settings.client.objects.findByLN(ObjectType.NONE, k)
                    if obj is None:
                        raise Exception("Unknown logical name:" + k)
                    val = reader.read(obj, v)
                    # try:
                    #     val = val.decode("utf-8")
                    # except:
                    #     pass
                    reader.showValue(v, val)
                    data_list.append(str(val))

                # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # data_list.append(now)


                # database = r"C:\sqlite\db\meter.db"
                # conn = sqlite3.connect(database)
                list_data.append(data_list)
                # df = pd.DataFrame(list_data, columns=['mea_number', 'Wh_total', 'Wh_on_peek', 'Wh_off_peek', 'version',
                #                                       'reboot_interval', 'program_id'])
                # df.to_sql(name='readmeter', con=conn, if_exists='append', index=False)


                if settings.outputFile:
                    settings.client.objects.save(settings.outputFile)
            else:
                reader.readAll(settings.outputFile)
        except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
            print(ex)
        except (KeyboardInterrupt, SystemExit, Exception) as ex:
            traceback.print_exc()
            if settings.media:
                settings.media.close()
            reader = None
        finally:
            if reader:
                try:
                    reader.close()
                except Exception:
                    traceback.print_exc()
            print("Ended. Press any key to continue.")


if __name__ == '__main__':
    database = r"C:\sqlite\db\meter.db"
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # data = c.execute('''SELECT * FROM meter''')
    data = c.execute('''SELECT * FROM reboot''')
    a = list()
    for row in data:
        a.append(row)
    for i in a:
        # ip_address = i[3]
        # base64_message = i[4]
        # base64_bytes = base64_message.encode('ascii')
        # password_bytes = base64.b64decode(base64_bytes)
        # password = password_bytes.decode('ascii')
        #
        # data_list = ['main.py', '-h', ip_address, '-p', '8000', '-c', '1', '-s', '1', '-a', 'Low', '-P', password,
        #              '-g', '0.0.96.1.0.255:2', '-g', '1.0.1.8.0.255:2', '-g', '1.0.1.8.1.255:2', '-g',
        #              '1.0.1.8.2.255:2', '-g', '0.0.96.1.6.255:2', '-g', '0.0.96.53.0.255:2', '-g', '0.0.96.1.3.255:2',
        #              '-o', 'C:\\Test_meter_reader\\test.xml']
        # sampleclient.main(data_list)

        ip_address = i[2]

        data_list = ['main.py', '-h', ip_address, '-p', '8000', '-c', '1', '-s', '1', '-a', 'Low', '-P', 'mea2091502',
                     '-g', '0.0.96.1.0.255:2', '-g', '0.0.96.53.0.255:2', '-o', 'C:\\Test_meter_reader\\test.xml']
        sampleclient.main(data_list)

    df = pd.DataFrame(list_data, columns=['mea_number', 'reboot_interval'])
    df.to_csv(r'C:\sqlite\db\excel_reboot\reboot_meter_non8.csv')
    conn.commit()
    conn.close()
