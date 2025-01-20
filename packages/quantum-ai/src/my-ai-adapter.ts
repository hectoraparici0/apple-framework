import { QuantumProcessor } from '@aeg/quantum-core';

        class MyAIAdapter {
            constructor(private quantumProcessor: QuantumProcessor) {}

            public processData(data: any): string {
                return this.quantumProcessor.process(data);
            }
        }

        export { MyAIAdapter };