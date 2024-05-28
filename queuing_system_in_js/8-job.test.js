import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './createPushNotificationsJobs';

describe('createPushNotificationsJobs', function () {
    let queue;

    before(function () {
        queue = kue.createQueue();
        kue.Job.rangeByType('push_notification_code_3', 'active', 0, 100, 'asc', (err, selectedJobs) => {
            selectedJobs.forEach((job) => job.remove());
        });
        queue.testMode.enter();
    });

    afterEach(function () {
        queue.testMode.clear();
    });

    after(function () {
        queue.testMode.exit();
    });

    it('should display an error message if jobs is not an array', function () {
        expect(() => createPushNotificationsJobs('not an array', queue)).to.throw(Error, 'Jobs is not an array');
    });

    it('should create two new jobs to the queue', function () {
        const jobs = [
            { phoneNumber: '1234567890', message: 'This is the code 1' },
            { phoneNumber: '0987654321', message: 'This is the code 2' },
        ];

        createPushNotificationsJobs(jobs, queue);

        expect(queue.testMode.jobs.length).to.equal(2);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[0].data).to.eql(jobs[0]);
        expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[1].data).to.eql(jobs[1]);
    });
});
