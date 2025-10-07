from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Court

class Command(BaseCommand):
    help = 'Populate database with Indian courts data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating Indian courts...'))
        
        courts_data = [
            # Supreme Court of India
            {
                'name': 'Supreme Court of India',
                'court_type': 'SC',
                'location': 'New Delhi',
                'state': 'Delhi',
                'address': 'Tilak Marg, New Delhi - 110001',
                'contact_info': 'Phone: 011-23388922, 011-23388942'
            },
            
            # High Courts
            {
                'name': 'Delhi High Court',
                'court_type': 'HC',
                'location': 'New Delhi',
                'state': 'Delhi',
                'address': 'Sher Shah Road, New Delhi - 110503',
                'contact_info': 'Phone: 011-23358757'
            },
            {
                'name': 'Bombay High Court',
                'court_type': 'HC',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Fort, Mumbai - 400001',
                'contact_info': 'Phone: 022-22620578'
            },
            {
                'name': 'Madras High Court',
                'court_type': 'HC',
                'location': 'Chennai',
                'state': 'Tamil Nadu',
                'address': 'High Court Buildings, Chennai - 600104',
                'contact_info': 'Phone: 044-25211415'
            },
            {
                'name': 'Calcutta High Court',
                'court_type': 'HC',
                'location': 'Kolkata',
                'state': 'West Bengal',
                'address': 'Esplanade Row, Kolkata - 700001',
                'contact_info': 'Phone: 033-22523839'
            },
            {
                'name': 'Karnataka High Court',
                'court_type': 'HC',
                'location': 'Bangalore',
                'state': 'Karnataka',
                'address': 'Attara Kacheri Road, Bangalore - 560001',
                'contact_info': 'Phone: 080-22212161'
            },
            {
                'name': 'Kerala High Court',
                'court_type': 'HC',
                'location': 'Kochi',
                'state': 'Kerala',
                'address': 'High Court P.O, Kochi - 682031',
                'contact_info': 'Phone: 0484-2391020'
            },
            {
                'name': 'Allahabad High Court',
                'court_type': 'HC',
                'location': 'Prayagraj',
                'state': 'Uttar Pradesh',
                'address': 'Kutchery Road, Prayagraj - 211001',
                'contact_info': 'Phone: 0532-2421481'
            },
            {
                'name': 'Rajasthan High Court',
                'court_type': 'HC',
                'location': 'Jodhpur',
                'state': 'Rajasthan',
                'address': 'High Court Road, Jodhpur - 342001',
                'contact_info': 'Phone: 0291-2543536'
            },
            {
                'name': 'Punjab and Haryana High Court',
                'court_type': 'HC',
                'location': 'Chandigarh',
                'state': 'Chandigarh',
                'address': 'Sector 1, Chandigarh - 160001',
                'contact_info': 'Phone: 0172-2740241'
            },
            
            # District Courts - Delhi
            {
                'name': 'Patiala House Courts Complex',
                'court_type': 'DC',
                'location': 'New Delhi',
                'state': 'Delhi',
                'address': 'Patiala House, New Delhi - 110001',
                'contact_info': 'Phone: 011-23073431'
            },
            {
                'name': 'Tis Hazari Courts',
                'court_type': 'DC',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Tis Hazari, Delhi - 110054',
                'contact_info': 'Phone: 011-23912345'
            },
            {
                'name': 'Karkardooma Courts',
                'court_type': 'DC',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Karkardooma, Delhi - 110032',
                'contact_info': 'Phone: 011-22151234'
            },
            {
                'name': 'Dwarka Courts',
                'court_type': 'DC',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Sector 10, Dwarka, Delhi - 110075',
                'contact_info': 'Phone: 011-25081234'
            },
            {
                'name': 'Rohini Courts',
                'court_type': 'DC',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Sector 14, Rohini, Delhi - 110085',
                'contact_info': 'Phone: 011-27551234'
            },
            
            # District Courts - Mumbai
            {
                'name': 'City Civil and Sessions Court, Mumbai',
                'court_type': 'DC',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Maharashtra Chambers, Mumbai - 400001',
                'contact_info': 'Phone: 022-22621234'
            },
            {
                'name': 'Additional Sessions Court, Borivali',
                'court_type': 'DC',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Borivali (W), Mumbai - 400092',
                'contact_info': 'Phone: 022-28911234'
            },
            {
                'name': 'Additional Sessions Court, Andheri',
                'court_type': 'DC',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Andheri (E), Mumbai - 400069',
                'contact_info': 'Phone: 022-26831234'
            },
            
            # Sessions Courts
            {
                'name': 'Sessions Court, Bangalore',
                'court_type': 'SC_MAG',
                'location': 'Bangalore',
                'state': 'Karnataka',
                'address': 'Bangalore City Court Complex - 560001',
                'contact_info': 'Phone: 080-22871234'
            },
            {
                'name': 'Sessions Court, Chennai',
                'court_type': 'SC_MAG',
                'location': 'Chennai',
                'state': 'Tamil Nadu',
                'address': 'Chennai City Court Complex - 600001',
                'contact_info': 'Phone: 044-28451234'
            },
            {
                'name': 'Sessions Court, Pune',
                'court_type': 'SC_MAG',
                'location': 'Pune',
                'state': 'Maharashtra',
                'address': 'Shivajinagar, Pune - 411005',
                'contact_info': 'Phone: 020-25531234'
            },
            
            # Magistrate Courts
            {
                'name': 'Chief Metropolitan Magistrate Court, Delhi',
                'court_type': 'CJM',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Tis Hazari Courts, Delhi - 110054',
                'contact_info': 'Phone: 011-23912345'
            },
            {
                'name': 'Metropolitan Magistrate Court, Mumbai',
                'court_type': 'MAG',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Bandra Court, Mumbai - 400050',
                'contact_info': 'Phone: 022-26451234'
            },
            {
                'name': 'Judicial Magistrate First Class, Gurgaon',
                'court_type': 'JMFC',
                'location': 'Gurgaon',
                'state': 'Haryana',
                'address': 'Mini Secretariat, Gurgaon - 122001',
                'contact_info': 'Phone: 0124-2321234'
            },
            
            # Family Courts
            {
                'name': 'Family Court, Delhi',
                'court_type': 'FAMILY',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Tis Hazari Courts, Delhi - 110054',
                'contact_info': 'Phone: 011-23915678'
            },
            {
                'name': 'Family Court, Mumbai',
                'court_type': 'FAMILY',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Bandra Court Complex, Mumbai - 400050',
                'contact_info': 'Phone: 022-26455678'
            },
            {
                'name': 'Family Court, Bangalore',
                'court_type': 'FAMILY',
                'location': 'Bangalore',
                'state': 'Karnataka',
                'address': 'City Court Complex, Bangalore - 560001',
                'contact_info': 'Phone: 080-22875678'
            },
            
            # Consumer Courts
            {
                'name': 'National Consumer Disputes Redressal Commission',
                'court_type': 'CONSUMER',
                'location': 'New Delhi',
                'state': 'Delhi',
                'address': 'Upbhokta Nyay Bhawan, New Delhi - 110001',
                'contact_info': 'Phone: 011-23236300'
            },
            {
                'name': 'State Consumer Disputes Redressal Commission, Delhi',
                'court_type': 'CONSUMER',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'B-1/10, Ardee City, Gurgaon - 122003',
                'contact_info': 'Phone: 011-28335200'
            },
            {
                'name': 'District Consumer Forum, Mumbai',
                'court_type': 'CONSUMER',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Tardeo, Mumbai - 400034',
                'contact_info': 'Phone: 022-24951234'
            },
            
            # Labour Courts
            {
                'name': 'Labour Court, Delhi',
                'court_type': 'LABOUR',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Karkardooma Courts, Delhi - 110032',
                'contact_info': 'Phone: 011-22155678'
            },
            {
                'name': 'Industrial Tribunal, Mumbai',
                'court_type': 'LABOUR',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Ballard Estate, Mumbai - 400001',
                'contact_info': 'Phone: 022-22615678'
            },
            
            # Tribunals
            {
                'name': 'National Green Tribunal',
                'court_type': 'TRIBUNAL',
                'location': 'New Delhi',
                'state': 'Delhi',
                'address': 'Faridkot House, New Delhi - 110003',
                'contact_info': 'Phone: 011-24695174'
            },
            {
                'name': 'Income Tax Appellate Tribunal',
                'court_type': 'TRIBUNAL',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Aayakar Bhawan, New Delhi - 110002',
                'contact_info': 'Phone: 011-23738481'
            },
            {
                'name': 'Central Administrative Tribunal',
                'court_type': 'TRIBUNAL',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Copernicus Marg, New Delhi - 110001',
                'contact_info': 'Phone: 011-23388546'
            },
            
            # Debts Recovery Tribunals
            {
                'name': 'Debts Recovery Tribunal, Delhi',
                'court_type': 'DEBTS',
                'location': 'Delhi',
                'state': 'Delhi',
                'address': 'Jamnagar House, New Delhi - 110011',
                'contact_info': 'Phone: 011-23013050'
            },
            {
                'name': 'Debts Recovery Tribunal, Mumbai',
                'court_type': 'DEBTS',
                'location': 'Mumbai',
                'state': 'Maharashtra',
                'address': 'Ballard Estate, Mumbai - 400001',
                'contact_info': 'Phone: 022-22651234'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        with transaction.atomic():
            for court_data in courts_data:
                court, created = Court.objects.get_or_create(
                    name=court_data['name'],
                    court_type=court_data['court_type'],
                    location=court_data['location'],
                    state=court_data['state'],
                    defaults={
                        'address': court_data.get('address', ''),
                        'contact_info': court_data.get('contact_info', ''),
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f"✅ Created: {court.name}")
                else:
                    # Update existing court with new information
                    court.address = court_data.get('address', court.address)
                    court.contact_info = court_data.get('contact_info', court.contact_info)
                    court.save()
                    updated_count += 1
                    self.stdout.write(f"🔄 Updated: {court.name}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully populated courts database!\n'
                f'📊 Summary:\n'
                f'   - Created: {created_count} courts\n'
                f'   - Updated: {updated_count} courts\n'
                f'   - Total: {created_count + updated_count} courts\n'
                f'\n🏛️ Court Types Added:\n'
                f'   - Supreme Court: 1\n'
                f'   - High Courts: 9\n'
                f'   - District Courts: 8\n'
                f'   - Sessions Courts: 3\n'
                f'   - Magistrate Courts: 3\n'
                f'   - Family Courts: 3\n'
                f'   - Consumer Courts: 3\n'
                f'   - Labour Courts: 2\n'
                f'   - Tribunals: 3\n'
                f'   - Debts Recovery Tribunals: 2\n'
                f'\n🗺️ States/UTs Covered:\n'
                f'   Delhi, Maharashtra, Tamil Nadu, West Bengal,\n'
                f'   Karnataka, Kerala, Uttar Pradesh, Rajasthan,\n'
                f'   Chandigarh, Haryana\n'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                f'\n💡 Next Steps:\n'
                f'   1. Run: python manage.py createsuperuser (if not done)\n'
                f'   2. Login to admin panel to manage courts\n'
                f'   3. Start creating clients and cases\n'
                f'   4. Explore the Electronic Diary features!\n'
            )
        )